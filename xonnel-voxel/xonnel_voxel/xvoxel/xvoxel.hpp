#pragma once

#include <cstddef>
#include <cstdint>
#include <unordered_map>
#include <vector>



struct XVoxelVert
{
    float x;
    float y;
    float z;
};



struct XVoxelFace
{
    std::uint32_t i0;
    std::uint32_t i1;
    std::uint32_t i2;
    std::uint32_t i3;
};



struct XVoxelEdge
{
    std::uint32_t i0;
    std::uint32_t i1;
};



class XVoxel
{
public:
    XVoxel(
        const float* array,
        std::size_t w,
        std::size_t h,
        std::size_t d,
        float tres = 1.0f,
        float sx = 1.0f,
        float sy = 1.0f,
        float sz = 1.0f,
        float ox = 0.0f,
        float oy = 0.0f,
        float oz = 0.0f
    );

    const std::vector<XVoxelVert>& verts();
    const std::vector<XVoxelFace>& faces();
    const std::vector<XVoxelEdge>& edges();

private:
    struct IVec3
    {
        int x;
        int y;
        int z;

        bool operator==(const IVec3& other) const
        {
            return x == other.x && y == other.y && z == other.z;
        }
    };

    struct IVec3Hash
    {
        std::size_t operator()(const IVec3& v) const
        {
            std::size_t h1 = std::hash<int>{}(v.x);
            std::size_t h2 = std::hash<int>{}(v.y);
            std::size_t h3 = std::hash<int>{}(v.z);
            return h1 ^ (h2 << 1) ^ (h3 << 2);
        }
    };

    struct EdgeKey
    {
        std::uint32_t a;
        std::uint32_t b;

        bool operator==(const EdgeKey& other) const
        {
            return a == other.a && b == other.b;
        }
    };

    struct EdgeKeyHash
    {
        std::size_t operator()(const EdgeKey& e) const
        {
            std::size_t h1 = std::hash<std::uint32_t>{}(e.a);
            std::size_t h2 = std::hash<std::uint32_t>{}(e.b);
            return h1 ^ (h2 << 1);
        }
    };

private:
    void process();

    bool in_bounds(int x, int y, int z) const;
    bool is_solid(int x, int y, int z) const;
    std::size_t index(std::size_t x, std::size_t y, std::size_t z) const;

    std::uint32_t add_vert(int gx, int gy, int gz);
    void add_edge(std::uint32_t a, std::uint32_t b);
    void add_face_from_std(
        int x,
        int y,
        int z,
        int face_id
    );

private:
    const float* array_;
    std::size_t w_;
    std::size_t h_;
    std::size_t d_;

    float tres_;

    float sx_;
    float sy_;
    float sz_;

    float ox_;
    float oy_;
    float oz_;

    bool processed_;

    std::vector<XVoxelVert> verts_;
    std::vector<XVoxelFace> faces_;
    std::vector<XVoxelEdge> edges_;

    std::unordered_map<IVec3, std::uint32_t, IVec3Hash> vert_map_;
    std::unordered_map<EdgeKey, std::uint32_t, EdgeKeyHash> edge_map_;
};



extern "C"
{
    __declspec(dllexport) XVoxel* xvoxel_create(
        const float* array,
        std::size_t w,
        std::size_t h,
        std::size_t d,
        float tres,
        float sx,
        float sy,
        float sz,
        float ox,
        float oy,
        float oz
    );

    __declspec(dllexport) void xvoxel_destroy(XVoxel* obj);

    __declspec(dllexport) std::size_t xvoxel_vert_count(XVoxel* obj);
    __declspec(dllexport) std::size_t xvoxel_face_count(XVoxel* obj);
    __declspec(dllexport) std::size_t xvoxel_edge_count(XVoxel* obj);

    __declspec(dllexport) void xvoxel_copy_verts(XVoxel* obj, float* out_xyz);
    __declspec(dllexport) void xvoxel_copy_faces(XVoxel* obj, std::uint32_t* out_i4);
    __declspec(dllexport) void xvoxel_copy_edges(XVoxel* obj, std::uint32_t* out_i2);
}