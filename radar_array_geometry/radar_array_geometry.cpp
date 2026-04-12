// radar_array_geometry.cpp
// -------------------------------------------------------------
// 阵列几何 + DBF 校准矩阵 + 导向矢量实现
// -------------------------------------------------------------

#include "radar_array_geometry.h"
#include <cmath>
#include <cstdio>

namespace RadarArray
{
    // ================= 可调参数区域（硬件相关，都放这里） =================

    // 基本间距（mm）
    static constexpr float BASE_SPACING_MM = 7.2f;

    // 工作频率（Hz）——可运行时修改
    static float g_fc_hz = 77.5e9f;   // 77.5 GHz (Was 79.5e9f)

    // ---- 物理 RX 阵列：与你 MATLAB 代码一致 ----
    // rx_multipliers = [-8, -4, -1, 0] * 7.2mm, y=0
    static const Antenna2D RX_ARRAY[] =
    {
        { -8.0f * BASE_SPACING_MM, 0.0f }, // RX1
        { -4.0f * BASE_SPACING_MM, 0.0f }, // RX2
        { -1.0f * BASE_SPACING_MM, 0.0f }, // RX3
        {  0.0f * BASE_SPACING_MM, 0.0f }, // RX4
    };
    static constexpr int N_RX = sizeof(RX_ARRAY) / sizeof(RX_ARRAY[0]);

    // ---- 物理 TX 阵列：与你 MATLAB 代码一致 ----
    // tx_x_multipliers = [0, 4, 8]
    // tx_y_multipliers = [2, 1, 0]
    static const Antenna2D TX_ARRAY[] =
    {
        { 0.0f * BASE_SPACING_MM, 2.0f * BASE_SPACING_MM }, // TX1
        { 4.0f * BASE_SPACING_MM, 1.0f * BASE_SPACING_MM }, // TX2
        { 8.0f * BASE_SPACING_MM, 0.0f * BASE_SPACING_MM }, // TX3
    };
    static constexpr int N_TX = sizeof(TX_ARRAY) / sizeof(TX_ARRAY[0]);

    // ---- DBF 校准矩阵 H_cal(tx,rx) ----
    // 默认全 1+0j（无校准）。实际标定后在这里填入每个通道的增益和相位。
    //
    // 例如：
    //   TX1-RX1  幅度 0.98, 相位 +5°  ->  0.98 * exp(j*5°)
    //   TX1-RX2  幅度 1.02, 相位 -3°
    //   ...
    //
    // 你可以直接改下面数组里的复数值作为“标定表”。
    static std::complex<float> g_calib_matrix[N_TX][N_RX] =
    {
        // TX1: [RX1, RX2, RX3, RX4]
        {
            {1.0f, 0.0f},   // TX1-RX1
            {1.0f, 0.0f},   // TX1-RX2
            {1.0f, 0.0f},   // TX1-RX3
            {1.0f, 0.0f},   // TX1-RX4
        },
        // TX2
        {
            {1.0f, 0.0f},   // TX2-RX1
            {1.0f, 0.0f},   // TX2-RX2
            {1.0f, 0.0f},   // TX2-RX3
            {1.0f, 0.0f},   // TX2-RX4
        },
        // TX3
        {
            {1.0f, 0.0f},   // TX3-RX1
            {1.0f, 0.0f},   // TX3-RX2
            {1.0f, 0.0f},   // TX3-RX3
            {1.0f, 0.0f},   // TX3-RX4
        }
    };

    // ================= 内部状态：虚拟阵列 =================

    static std::vector<VirtualAntenna> g_virtual_array;
    static bool g_initialized = false;

    // ================= 内部工具函数 =================

    inline float speed_of_light()
    {
        return 299792458.0f; // m/s
    }

    inline float wavelength_m()
    {
        return speed_of_light() / g_fc_hz;
    }

    inline float mm_to_m(float mm)
    {
        return mm * 1.0e-3f;
    }

    static void BuildVirtualArrayOnce()
    {
        if (g_initialized) return;

        g_virtual_array.clear();
        g_virtual_array.reserve(N_TX * N_RX);

        // 虚拟阵列顺序约定：
        // for tx = 0..N_TX-1
        //   for rx = 0..N_RX-1
        for (int tx = 0; tx < N_TX; ++tx)
        {
            for (int rx = 0; rx < N_RX; ++rx)
            {
                VirtualAntenna v{};
                v.x_mm = TX_ARRAY[tx].x_mm + RX_ARRAY[rx].x_mm;
                v.y_mm = -(TX_ARRAY[tx].y_mm + RX_ARRAY[rx].y_mm);
                v.tx_id = tx;
                v.rx_id = rx;

                g_virtual_array.push_back(v);
            }
        }

        g_initialized = true;
    }

    static void EnsureInitialized()
    {
        if (!g_initialized)
            BuildVirtualArrayOnce();
    }

    // ================== 对外接口实现 ====================

    int GetNumTx()
    {
        return N_TX;
    }

    int GetNumRx()
    {
        return N_RX;
    }

    int GetNumVirtual()
    {
        EnsureInitialized();
        return static_cast<int>(g_virtual_array.size());
    }

    const Antenna2D* GetTxArray(int& count)
    {
        count = N_TX;
        return TX_ARRAY;
    }

    const Antenna2D* GetRxArray(int& count)
    {
        count = N_RX;
        return RX_ARRAY;
    }

    const VirtualAntenna* GetVirtualArray(int& count)
    {
        EnsureInitialized();
        count = static_cast<int>(g_virtual_array.size());
        return g_virtual_array.data();
    }

    float GetWavelength_m()
    {
        return wavelength_m();
    }

    void SetFrequencyHz(float hz)
    {
        if (hz > 0.0f)
        {
            g_fc_hz = hz;
        }
    }

    float GetFrequencyHz()
    {
        return g_fc_hz;
    }

    // ================== 导向矢量 ====================

    void ComputeSteeringVector2D(float azimuth_rad,
                                 float elevation_rad,
                                 std::vector<std::complex<float>>& out_w)
    {
        EnsureInitialized();

        const float lambda = wavelength_m();
        const float k = 2.0f * 3.14159265358979f / lambda;

        const float cos_el = std::cos(elevation_rad);
        const float sin_el = std::sin(elevation_rad);
        const float sin_az = std::sin(azimuth_rad);

        float kx = k * cos_el * sin_az;
        float ky = k * sin_el;

        int nV = static_cast<int>(g_virtual_array.size());
        out_w.resize(nV);

        for (int i = 0; i < nV; ++i)
        {
            const auto& v = g_virtual_array[i];

            float x_m = mm_to_m(v.x_mm);
            float y_m = mm_to_m(v.y_mm);

            float phase = -(kx * x_m + ky * y_m);
            out_w[i] = std::complex<float>(std::cos(phase), std::sin(phase));
        }
    }

    void ComputeSteeringVectorAzimuth(float azimuth_rad,
                                      std::vector<std::complex<float>>& out_w)
    {
        ComputeSteeringVector2D(azimuth_rad, 0.0f, out_w);
    }

    // ================== 校准矩阵相关 ====================

    void GetCalibrationVector(std::vector<std::complex<float>>& calib)
    {
        EnsureInitialized();
        int nV = static_cast<int>(g_virtual_array.size());
        calib.resize(nV);

        for (int i = 0; i < nV; ++i)
        {
            const auto& v = g_virtual_array[i];
            calib[i] = g_calib_matrix[v.tx_id][v.rx_id];
        }
    }

    std::complex<float> GetCalibrationForVirtual(int virtual_idx)
    {
        EnsureInitialized();
        if (virtual_idx < 0 || virtual_idx >= (int)g_virtual_array.size())
            return std::complex<float>(1.0f, 0.0f);

        const auto& v = g_virtual_array[virtual_idx];
        return g_calib_matrix[v.tx_id][v.rx_id];
    }

    std::complex<float> GetCalibrationForTxRx(int tx_id, int rx_id)
    {
        if (tx_id < 0 || tx_id >= N_TX || rx_id < 0 || rx_id >= N_RX)
            return std::complex<float>(1.0f, 0.0f);
        return g_calib_matrix[tx_id][rx_id];
    }

    void SetCalibrationForTxRx(int tx_id, int rx_id, std::complex<float> val)
    {
        if (tx_id < 0 || tx_id >= N_TX || rx_id < 0 || rx_id >= N_RX)
            return;
        g_calib_matrix[tx_id][rx_id] = val;
    }

    // ================== 调试输出 ====================

    void DebugPrintGeometry()
    {
        EnsureInitialized();

        std::printf("========== Radar Array Geometry ==========\n");
        std::printf("Frequency: %.2f GHz\n", g_fc_hz / 1e9f);
        std::printf("Wavelength: %.4f mm\n", wavelength_m() * 1e3f);
        std::printf("Base spacing: %.2f mm\n", BASE_SPACING_MM);
        std::printf("\n");

        std::printf("TX Array (%d elements):\n", N_TX);
        for (int i = 0; i < N_TX; ++i)
        {
            std::printf("  TX%d: (%.2f, %.2f) mm\n",
                i + 1, TX_ARRAY[i].x_mm, TX_ARRAY[i].y_mm);
        }
        std::printf("\n");

        std::printf("RX Array (%d elements):\n", N_RX);
        for (int i = 0; i < N_RX; ++i)
        {
            std::printf("  RX%d: (%.2f, %.2f) mm\n",
                i + 1, RX_ARRAY[i].x_mm, RX_ARRAY[i].y_mm);
        }
        std::printf("\n");

        std::printf("Virtual Array (%d elements):\n", (int)g_virtual_array.size());
        for (size_t i = 0; i < g_virtual_array.size(); ++i)
        {
            const auto& v = g_virtual_array[i];
            std::printf("  V%zu: TX%d-RX%d at (%.2f, %.2f) mm, calib=(%.3f, %.3f)\n",
                i, v.tx_id + 1, v.rx_id + 1,
                v.x_mm, v.y_mm,
                g_calib_matrix[v.tx_id][v.rx_id].real(),
                g_calib_matrix[v.tx_id][v.rx_id].imag());
        }
        std::printf("==========================================\n");
    }

} // namespace RadarArray
