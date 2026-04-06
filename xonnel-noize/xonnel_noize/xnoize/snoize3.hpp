#pragma once

#include <cstddef>
#include <cstdint>

class SNoize3
{
public:
    explicit SNoize3(std::uint32_t seed = 0);

    void generate(
        float* out,
        std::size_t w,
        std::size_t h,
        std::size_t d,
        float scale = 64.0f,
        std::size_t octs = 1,
        float pers = 0.5f,
        float lacu = 2.0f,
        float offx = 0.0f,
        float offy = 0.0f,
        float offz = 0.0f,
        float norm0 = 0.0f,
        float norm1 = 1.0f
    ) const;

private:
    std::uint8_t perm_[512];

    static int fastfloor(float x);
    static float dot(const int* g, float x, float y, float z);

    void build_perm(std::uint32_t seed);
    float sample(float x, float y, float z) const;
};

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
    );
}