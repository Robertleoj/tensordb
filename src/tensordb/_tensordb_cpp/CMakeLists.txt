
set(FILES
    example.cpp
)

nanobind_add_module(_tensordb_cpp python.cpp ${FILES})

target_link_libraries(_tensordb_cpp PUBLIC spdlog::spdlog Tracy::TracyClient)

target_include_directories(_tensordb_cpp PUBLIC ../../include)
