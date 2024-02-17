
set(FILES
    example.cpp
)

nanobind_add_module(tensordb_cpp python.cpp ${FILES})

target_link_libraries(tensordb_cpp PUBLIC spdlog::spdlog Tracy::TracyClient)

target_include_directories(tensordb_cpp PUBLIC ../../include)
