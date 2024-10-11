#include <vector>

#include "contourklip.hpp"
#include "clipping.h"
#include "model_data.h"

std::vector<contourklip::Contour> wall_countours;

extern "C" void clipping_add_wall(struct wall *w) {
  contourklip::Contour contour;
  for(int i=0;i<4;i++) {
    contour.push_back({ w->verts[i].x, w->verts[i].y });
  }

  wall_countours.push_back(contour);
}