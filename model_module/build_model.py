import cffi
import os

if __name__ == '__main__':
  ffi = cffi.FFI()

  model_dir_path = os.path.join(os.path.dirname(__file__), '..', 'model')

  with open(os.path.join(model_dir_path, 'build', 'lib_model', 'model.h.preprocessed')) as f:
    ffi.cdef(f.read())
  
  ffi.set_source('_model',
    '#include "model.h"',
    libraries=['model'],
    library_dirs=[model_dir_path],
    include_dirs=[model_dir_path]
  )

  ffi.compile()