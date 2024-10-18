#include <vector>
#include <iostream>

#include "contourklip.hpp"
#include "clipping.h"
#include "model_data.h"

std::vector<contourklip::Contour> wall_countours;

extern "C" void clipping_add_wall(struct wall *w) {
  contourklip::Contour contour;
  for(int i=0;i<4;i++) {
    contour.push_back({ w->verts[i].x, w->verts[i].y });
  }
  contour.close();

  wall_countours.push_back(contour);
}

extern "C" polygon_t polygon_new() {
  return (void *) new contourklip::Contour;
}

extern "C" void polygon_free(polygon_t rect) {
  delete (contourklip::Contour *) rect;
}

extern "C" void polygon_add_point(polygon_t rect, struct vec point) {
  contourklip::Contour *contour = (contourklip::Contour *)rect;
  contour->push_back({ point.x, point.y });
}

extern "C" polygon_t polygon_union_rect(polygon_t polygon, polygon_t rect) {
  contourklip::Contour *rect_contour = (contourklip::Contour *) rect;
  rect_contour->close();
  if(polygon == NULL) {
    contourklip::Contour *result = new contourklip::Contour;
    // for(auto point = rect_contour->begin();point < rect_contour->end();point++) {
    //   // std::cout << "Copy point " << *point << std::endl;
    //   result->push_back(*point);
    // }
    *result = *rect_contour;
    return result;
  }

  contourklip::Contour *polygon_contour = (contourklip::Contour *) polygon;
  std::vector<contourklip::Contour> shape1{*polygon_contour};
  std::vector<contourklip::Contour> shape2{*rect_contour};
  std::vector<contourklip::Contour> result;

  if(contourklip::clip(shape1, shape2, result, contourklip::UNION)) {
    //std::cout << "union success with size: " << result.size() << std::endl;
    *((contourklip::Contour *)polygon) = result[0];
  } else {
    std::cout << "union failed" << std::endl;
  }

  return polygon;
}

extern "C" polygon_t polygon_clip_walls(polygon_t polygon) {
  contourklip::Contour *polygon_contour = (contourklip::Contour *) polygon;
  std::vector<contourklip::Contour> shape1{*polygon_contour};
  for(auto contour: wall_countours) {
    std::vector<contourklip::Contour> shape2{contour};
    std::vector<contourklip::Contour> result;
    
    if(contourklip::clip(shape1, shape2, result, contourklip::DIFFERENCE)) {
      if(result.size() == 0) {
        std::cout << "wall clip size 0";
        continue;
      }

      shape1.pop_back();
      size_t max_i=0;
      for(size_t i=0;i<result.size();i++) {
        if(result[i].size() > result[max_i].size()) {
          max_i = i;
        }
      }
      auto next = result[max_i];
      shape1.push_back(next);
      // }
    } else {
      std::cout << "wall clip failed" << std::endl;
    }

    *((contourklip::Contour *)polygon) = shape1[0];
  }

  return polygon;
}

// get polygon area with the shoelace formula
extern "C" float polygon_area(polygon_t polygon) {
  float area = 0;
  contourklip::Contour *polygon_contour = (contourklip::Contour *) polygon;
  for(std::size_t i=0;i<polygon_contour->size() - 1;i++) {
    auto first = (*polygon_contour)[i];
    auto second = (*polygon_contour)[i + 1];
    area += (first.point().y() + second.point().y()) * (first.point().x() - second.point().x());
  }
  return 0.5 * area;
}

void polygon_to_points(polygon_t polygon, struct vec **points, uint32_t *cnt) {
  contourklip::Contour *polygon_contour = (contourklip::Contour *) polygon;
  *cnt = polygon_contour->size();
  *points = (struct vec *) malloc(sizeof(struct vec) * polygon_contour->size());
  int i = 0;
  for(auto point = polygon_contour->begin(); point < polygon_contour->end(); point++) {
    (*points)[i] = (struct vec) { (float) point->point().x(), (float) point->point().y() };
    i++;
  }
}