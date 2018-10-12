cmake_minimum_required(VERSION 3.1 FATAL_ERROR)

project(TdExample VERSION 1.0 LANGUAGES CXX)

find_package(Td 1.3.0 REQUIRED)

add_executable(td_test td_test.cpp)
target_link_libraries(td_test PRIVATE Td::TdStatic)
set_property(TARGET td_test PROPERTY CXX_STANDARD 14)

add_executable(td_example td_example.cpp)
target_link_libraries(td_example PRIVATE Td::TdStatic)
set_property(TARGET td_example PROPERTY CXX_STANDARD 14)
