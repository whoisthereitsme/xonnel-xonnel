#include "snoize3.hpp"

#include <algorithm>
#include <cmath>
#include <memory>
#include <mutex>
#include <random>
#include <stdexcept>
#include <thread>
#include <unordered_map>
#include <vector>



static const int SNOIZE3_GRADS[12][3] =
{
    { 1, 1, 0 }, { -1, 1, 0 }, { 1, -1, 0 }, { -1, -1, 0 },
    { 1, 0, 1 }, { -1, 0, 1 }, { 1, 0, -1 }, { -1, 0, -1 },
    { 0, 1, 1 }, { 0, -1, 1 }, { 0, 1, -1 }, { 0, -1, -1 }
};



SNoize3::SNoize3(std::uint32_t seed)
{
    build_perm(seed);
}



void SNoize3::build_perm(std::uint32_t seed)
{
    std::uint8_t base[256];

    for (int i = 0; i < 256; ++i)
    {
        base[i] = static_cast<std::uint8_t>(i);
    }

    std::mt19937 rng(seed);
    std::shuffle(std::begin(base), std::end(base), rng);

    for (int i = 0; i < 256; ++i)
    {
        perm_[i] = base[i];
        perm_[256 + i] = base[i];
    }
}



int SNoize3::fastfloor(float x)
{
    const int i = static_cast<int>(x);
    return (x < static_cast<float>(i)) ? (i - 1) : i;
}



float SNoize3::dot(const int* g, float x, float y, float z)
{
    return static_cast<float>(g[0]) * x +
           static_cast<float>(g[1]) * y +
           static_cast<float>(g[2]) * z;
}



float SNoize3::sample(float x, float y, float z) const
{
    constexpr float F3 = 1.0f / 3.0f;
    constexpr float G3 = 1.0f / 6.0f;

    const float s = (x + y + z) * F3;
    const int i = fastfloor(x + s);
    const int j = fastfloor(y + s);
    const int k = fastfloor(z + s);

    const float t = static_cast<float>(i + j + k) * G3;
    const float X0 = static_cast<float>(i) - t;
    const float Y0 = static_cast<float>(j) - t;
    const float Z0 = static_cast<float>(k) - t;

    const float x0 = x - X0;
    const float y0 = y - Y0;
    const float z0 = z - Z0;

    int i1, j1, k1;
    int i2, j2, k2;

    if (x0 >= y0)
    {
        if (y0 >= z0)
        {
            i1 = 1; j1 = 0; k1 = 0;
            i2 = 1; j2 = 1; k2 = 0;
        }
        else if (x0 >= z0)
        {
            i1 = 1; j1 = 0; k1 = 0;
            i2 = 1; j2 = 0; k2 = 1;
        }
        else
        {
            i1 = 0; j1 = 0; k1 = 1;
            i2 = 1; j2 = 0; k2 = 1;
        }
    }
    else
    {
        if (y0 < z0)
        {
            i1 = 0; j1 = 0; k1 = 1;
            i2 = 0; j2 = 1; k2 = 1;
        }
        else if (x0 < z0)
        {
            i1 = 0; j1 = 1; k1 = 0;
            i2 = 0; j2 = 1; k2 = 1;
        }
        else
        {
            i1 = 0; j1 = 1; k1 = 0;
            i2 = 1; j2 = 1; k2 = 0;
        }
    }

    const float x1 = x0 - static_cast<float>(i1) + G3;
    const float y1 = y0 - static_cast<float>(j1) + G3;
    const float z1 = z0 - static_cast<float>(k1) + G3;

    const float x2 = x0 - static_cast<float>(i2) + 2.0f * G3;
    const float y2 = y0 - static_cast<float>(j2) + 2.0f * G3;
    const float z2 = z0 - static_cast<float>(k2) + 2.0f * G3;

    const float x3 = x0 - 1.0f + 3.0f * G3;
    const float y3 = y0 - 1.0f + 3.0f * G3;
    const float z3 = z0 - 1.0f + 3.0f * G3;

    const int ii = i & 255;
    const int jj = j & 255;
    const int kk = k & 255;

    const int gi0 = perm_[ii + perm_[jj + perm_[kk]]] % 12;
    const int gi1 = perm_[ii + i1 + perm_[jj + j1 + perm_[kk + k1]]] % 12;
    const int gi2 = perm_[ii + i2 + perm_[jj + j2 + perm_[kk + k2]]] % 12;
    const int gi3 = perm_[ii + 1 + perm_[jj + 1 + perm_[kk + 1]]] % 12;

    float n0 = 0.0f;
    float n1 = 0.0f;
    float n2 = 0.0f;
    float n3 = 0.0f;

    float t0 = 0.6f - x0 * x0 - y0 * y0 - z0 * z0;
    if (t0 > 0.0f)
    {
        t0 *= t0;
        n0 = t0 * t0 * dot(SNOIZE3_GRADS[gi0], x0, y0, z0);
    }

    float t1 = 0.6f - x1 * x1 - y1 * y1 - z1 * z1;
    if (t1 > 0.0f)
    {
        t1 *= t1;
        n1 = t1 * t1 * dot(SNOIZE3_GRADS[gi1], x1, y1, z1);
    }

    float t2 = 0.6f - x2 * x2 - y2 * y2 - z2 * z2;
    if (t2 > 0.0f)
    {
        t2 *= t2;
        n2 = t2 * t2 * dot(SNOIZE3_GRADS[gi2], x2, y2, z2);
    }

    float t3 = 0.6f - x3 * x3 - y3 * y3 - z3 * z3;
    if (t3 > 0.0f)
    {
        t3 *= t3;
        n3 = t3 * t3 * dot(SNOIZE3_GRADS[gi3], x3, y3, z3);
    }

    return 32.0f * (n0 + n1 + n2 + n3);
}



void SNoize3::generate(
    float* out,
    std::size_t w,
    std::size_t h,
    std::size_t d,
    float scale,
    std::size_t octs,
    float pers,
    float lacu,
    float offx,
    float offy,
    float offz,
    float norm0,
    float norm1
) const
{
    if (out == nullptr) throw std::invalid_argument("out is null");
    if (w == 0 || h == 0 || d == 0) throw std::invalid_argument("w/h/d invalid");
    if (scale <= 0.0f) throw std::invalid_argument("scale invalid");
    if (octs == 0) throw std::invalid_argument("octs invalid");
    if (lacu <= 0.0f) throw std::invalid_argument("lacu invalid");

    const std::size_t hw = std::thread::hardware_concurrency();
    const std::size_t nthreads = hw > 0 ? hw : 4;
    const std::size_t slices_per_thread = (d + nthreads - 1) / nthreads;

    std::vector<float> mins(nthreads);
    std::vector<float> maxs(nthreads);
    std::vector<std::thread> threads;
    threads.reserve(nthreads);

    auto worker = [&](std::size_t tid, std::size_t z0, std::size_t z1)
    {
        bool first = true;
        float mn = 0.0f;
        float mx = 0.0f;

        for (std::size_t z = z0; z < z1; ++z)
        {
            for (std::size_t y = 0; y < h; ++y)
            {
                for (std::size_t x = 0; x < w; ++x)
                {
                    float amp = 1.0f;
                    float freq = 1.0f;
                    float val = 0.0f;
                    float amp_sum = 0.0f;

                    for (std::size_t o = 0; o < octs; ++o)
                    {
                        const float sx = (static_cast<float>(x) + offx) / scale * freq;
                        const float sy = (static_cast<float>(y) + offy) / scale * freq;
                        const float sz = (static_cast<float>(z) + offz) / scale * freq;

                        val += sample(sx, sy, sz) * amp;
                        amp_sum += amp;

                        amp *= pers;
                        freq *= lacu;
                    }

                    if (amp_sum > 0.0f)
                    {
                        val /= amp_sum;
                    }

                    const std::size_t i = (z * h + y) * w + x;
                    out[i] = val;

                    if (first)
                    {
                        mn = val;
                        mx = val;
                        first = false;
                    }
                    else
                    {
                        if (val < mn) mn = val;
                        if (val > mx) mx = val;
                    }
                }
            }
        }

        mins[tid] = mn;
        maxs[tid] = mx;
    };

    for (std::size_t tid = 0; tid < nthreads; ++tid)
    {
        const std::size_t z0 = tid * slices_per_thread;
        const std::size_t z1 = std::min(z0 + slices_per_thread, d);

        if (z0 >= z1)
        {
            mins[tid] = 0.0f;
            maxs[tid] = 0.0f;
            continue;
        }

        threads.emplace_back(worker, tid, z0, z1);
    }

    for (auto& t : threads)
    {
        t.join();
    }

    bool first = true;
    float mn = 0.0f;
    float mx = 0.0f;

    for (std::size_t tid = 0; tid < nthreads; ++tid)
    {
        const std::size_t z0 = tid * slices_per_thread;
        const std::size_t z1 = std::min(z0 + slices_per_thread, d);

        if (z0 >= z1) continue;

        if (first)
        {
            mn = mins[tid];
            mx = maxs[tid];
            first = false;
        }
        else
        {
            if (mins[tid] < mn) mn = mins[tid];
            if (maxs[tid] > mx) mx = maxs[tid];
        }
    }

    const float src_rng = mx - mn;
    const float dst_rng = norm1 - norm0;
    const std::size_t size = w * h * d;

    if (src_rng > 0.0f)
    {
        for (std::size_t i = 0; i < size; ++i)
        {
            out[i] = norm0 + ((out[i] - mn) / src_rng) * dst_rng;
        }
    }
    else
    {
        const float mid = (norm0 + norm1) * 0.5f;
        for (std::size_t i = 0; i < size; ++i)
        {
            out[i] = mid;
        }
    }
}



extern "C"
{
    __declspec(dllexport) void snoize3(
        float* out,
        std::size_t w,
        std::size_t h,
        std::size_t d,
        std::uint32_t seed,
        float scale,
        std::size_t octs,
        float pers,
        float lacu,
        float offx,
        float offy,
        float offz,
        float norm0,
        float norm1
    )
    {
        static std::unordered_map<std::uint32_t, std::shared_ptr<SNoize3>> cache;
        static std::mutex mutex;

        std::shared_ptr<SNoize3> inst;

        {
            std::lock_guard<std::mutex> lock(mutex);

            auto it = cache.find(seed);

            if (it == cache.end())
            {
                inst = std::make_shared<SNoize3>(seed);
                cache.emplace(seed, inst);
            }
            else
            {
                inst = it->second;
            }
        }

        inst->generate(out, w, h, d, scale, octs, pers, lacu, offx, offy, offz, norm0, norm1);
    }
}