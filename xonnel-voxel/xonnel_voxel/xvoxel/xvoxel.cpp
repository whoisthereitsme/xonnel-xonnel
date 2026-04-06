#include "xvoxel.hpp"

#include <algorithm>
#include <stdexcept>



XVoxel::XVoxel(
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
)
    : array_(array),
      w_(w),
      h_(h),
      d_(d),
      tres_(tres),
      sx_(sx),
      sy_(sy),
      sz_(sz),
      ox_(ox),
      oy_(oy),
      oz_(oz),
      processed_(false)
{
    if (array_ == nullptr) throw std::invalid_argument("array is null");
    if (w_ == 0 || h_ == 0 || d_ == 0) throw std::invalid_argument("w/h/d invalid");
    if (sx_ <= 0.0f || sy_ <= 0.0f || sz_ <= 0.0f) throw std::invalid_argument("size invalid");
}



const std::vector<XVoxelVert>& XVoxel::verts()
{
    process();
    return verts_;
}



const std::vector<XVoxelFace>& XVoxel::faces()
{
    process();
    return faces_;
}



const std::vector<XVoxelEdge>& XVoxel::edges()
{
    process();
    return edges_;
}



bool XVoxel::in_bounds(int x, int y, int z) const
{
    return
        x >= 0 && x < static_cast<int>(w_) &&
        y >= 0 && y < static_cast<int>(h_) &&
        z >= 0 && z < static_cast<int>(d_);
}



bool XVoxel::is_solid(int x, int y, int z) const
{
    if (!in_bounds(x, y, z))
    {
        return false;
    }

    return array_[index(
        static_cast<std::size_t>(x),
        static_cast<std::size_t>(y),
        static_cast<std::size_t>(z)
    )] >= tres_;
}



std::size_t XVoxel::index(std::size_t x, std::size_t y, std::size_t z) const
{
    return z * (w_ * h_) + y * w_ + x;
}



/*
standard voxel corners in local voxel space:

0 = (0,0,0)
1 = (1,0,0)
2 = (1,1,0)
3 = (0,1,0)
4 = (0,0,1)
5 = (1,0,1)
6 = (1,1,1)
7 = (0,1,1)

faces:
0 = -x
1 = +x
2 = -y
3 = +y
4 = -z
5 = +z
*/
std::uint32_t XVoxel::add_vert(int gx, int gy, int gz)
{
    IVec3 key{gx, gy, gz};

    auto it = vert_map_.find(key);
    if (it != vert_map_.end())
    {
        return it->second;
    }

    const std::uint32_t idx = static_cast<std::uint32_t>(verts_.size());

    XVoxelVert v;
    v.x = ox_ + static_cast<float>(gx) * sx_;
    v.y = oy_ + static_cast<float>(gy) * sy_;
    v.z = oz_ + static_cast<float>(gz) * sz_;

    verts_.push_back(v);
    vert_map_.emplace(key, idx);

    return idx;
}



void XVoxel::add_edge(std::uint32_t a, std::uint32_t b)
{
    if (a > b)
    {
        std::swap(a, b);
    }

    EdgeKey key{a, b};

    if (edge_map_.find(key) != edge_map_.end())
    {
        return;
    }

    XVoxelEdge e;
    e.i0 = a;
    e.i1 = b;
    edges_.push_back(e);

    edge_map_.emplace(key, static_cast<std::uint32_t>(edges_.size() - 1));
}



void XVoxel::add_face_from_std(
    int x,
    int y,
    int z,
    int face_id
)
{
    static const int cube_verts[8][3] =
    {
        {0, 0, 0}, // 0
        {1, 0, 0}, // 1
        {1, 1, 0}, // 2
        {0, 1, 0}, // 3
        {0, 0, 1}, // 4
        {1, 0, 1}, // 5
        {1, 1, 1}, // 6
        {0, 1, 1}  // 7
    };

    static const int cube_faces[6][4] =
    {
        {0, 4, 7, 3}, // -x
        {1, 2, 6, 5}, // +x
        {0, 1, 5, 4}, // -y
        {3, 7, 6, 2}, // +y
        {0, 3, 2, 1}, // -z
        {4, 5, 6, 7}  // +z
    };

    const int a = cube_faces[face_id][0];
    const int b = cube_faces[face_id][1];
    const int c = cube_faces[face_id][2];
    const int d = cube_faces[face_id][3];

    const std::uint32_t i0 = add_vert(
        x + cube_verts[a][0],
        y + cube_verts[a][1],
        z + cube_verts[a][2]
    );

    const std::uint32_t i1 = add_vert(
        x + cube_verts[b][0],
        y + cube_verts[b][1],
        z + cube_verts[b][2]
    );

    const std::uint32_t i2 = add_vert(
        x + cube_verts[c][0],
        y + cube_verts[c][1],
        z + cube_verts[c][2]
    );

    const std::uint32_t i3 = add_vert(
        x + cube_verts[d][0],
        y + cube_verts[d][1],
        z + cube_verts[d][2]
    );

    XVoxelFace f;
    f.i0 = i0;
    f.i1 = i1;
    f.i2 = i2;
    f.i3 = i3;
    faces_.push_back(f);

    add_edge(i0, i1);
    add_edge(i1, i2);
    add_edge(i2, i3);
    add_edge(i3, i0);
}



void XVoxel::process()
{
    if (processed_)
    {
        return;
    }

    verts_.clear();
    faces_.clear();
    edges_.clear();
    vert_map_.clear();
    edge_map_.clear();

    for (std::size_t z = 0; z < d_; ++z)
    {
        for (std::size_t y = 0; y < h_; ++y)
        {
            for (std::size_t x = 0; x < w_; ++x)
            {
                const int xi = static_cast<int>(x);
                const int yi = static_cast<int>(y);
                const int zi = static_cast<int>(z);

                if (!is_solid(xi, yi, zi))
                {
                    continue;
                }

                if (!is_solid(xi - 1, yi, zi)) add_face_from_std(xi, yi, zi, 0);
                if (!is_solid(xi + 1, yi, zi)) add_face_from_std(xi, yi, zi, 1);
                if (!is_solid(xi, yi - 1, zi)) add_face_from_std(xi, yi, zi, 2);
                if (!is_solid(xi, yi + 1, zi)) add_face_from_std(xi, yi, zi, 3);
                if (!is_solid(xi, yi, zi - 1)) add_face_from_std(xi, yi, zi, 4);
                if (!is_solid(xi, yi, zi + 1)) add_face_from_std(xi, yi, zi, 5);
            }
        }
    }

    processed_ = true;
}



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
    )
    {
        return new XVoxel(array, w, h, d, tres, sx, sy, sz, ox, oy, oz);
    }



    __declspec(dllexport) void xvoxel_destroy(XVoxel* obj)
    {
        delete obj;
    }



    __declspec(dllexport) std::size_t xvoxel_vert_count(XVoxel* obj)
    {
        if (obj == nullptr) return 0;
        return obj->verts().size();
    }



    __declspec(dllexport) std::size_t xvoxel_face_count(XVoxel* obj)
    {
        if (obj == nullptr) return 0;
        return obj->faces().size();
    }



    __declspec(dllexport) std::size_t xvoxel_edge_count(XVoxel* obj)
    {
        if (obj == nullptr) return 0;
        return obj->edges().size();
    }



    __declspec(dllexport) void xvoxel_copy_verts(XVoxel* obj, float* out_xyz)
    {
        if (obj == nullptr) throw std::invalid_argument("obj is null");
        if (out_xyz == nullptr) throw std::invalid_argument("out_xyz is null");

        const auto& verts = obj->verts();

        for (std::size_t i = 0; i < verts.size(); ++i)
        {
            out_xyz[i * 3 + 0] = verts[i].x;
            out_xyz[i * 3 + 1] = verts[i].y;
            out_xyz[i * 3 + 2] = verts[i].z;
        }
    }



    __declspec(dllexport) void xvoxel_copy_faces(XVoxel* obj, std::uint32_t* out_i4)
    {
        if (obj == nullptr) throw std::invalid_argument("obj is null");
        if (out_i4 == nullptr) throw std::invalid_argument("out_i4 is null");

        const auto& faces = obj->faces();

        for (std::size_t i = 0; i < faces.size(); ++i)
        {
            out_i4[i * 4 + 0] = faces[i].i0;
            out_i4[i * 4 + 1] = faces[i].i1;
            out_i4[i * 4 + 2] = faces[i].i2;
            out_i4[i * 4 + 3] = faces[i].i3;
        }
    }



    __declspec(dllexport) void xvoxel_copy_edges(XVoxel* obj, std::uint32_t* out_i2)
    {
        if (obj == nullptr) throw std::invalid_argument("obj is null");
        if (out_i2 == nullptr) throw std::invalid_argument("out_i2 is null");

        const auto& edges = obj->edges();

        for (std::size_t i = 0; i < edges.size(); ++i)
        {
            out_i2[i * 2 + 0] = edges[i].i0;
            out_i2[i * 2 + 1] = edges[i].i1;
        }
    }
}