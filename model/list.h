#include <stdint.h>

#define LIST_HEAD(name, type) \
  struct name {               \
    struct type *first;       \
    uint32_t cnt;             \
  }

#define LIST_HEAD_INIT() { NULL, 0 }

#define LIST_ENTRY(type)    \
  struct {                  \
    struct type *list_next;  \
  }                         

#define LIST_INSERT(headp, elem, field)       \
  do {                                        \
    (elem)->field.list_next = (headp)->first;             \
    (headp)->first = (elem);                    \
    (headp)->cnt++;                             \
  } while(0);

#define LIST_FOREACH(var, headp, field) \
  for((var) = (headp)->first; (var); (var) = (var)->field.list_next)
