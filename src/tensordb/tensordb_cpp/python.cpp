#include "../../../include/tensordb_cpp/example.hpp"
#include <nanobind/nanobind.h>

// NOTE: This sets compile time level. In addition, you need to set the
// runtime level low enough to show these (e.g. trace for everything)
#define SPDLOG_ACTIVE_LEVEL SPDLOG_LEVEL_INFO

#include <fstream>
#include <spdlog/spdlog.h>

namespace nb = nanobind;
using namespace nb::literals;

using namespace tensordb;

NB_MODULE(tensordb_cpp, m) {
  m.doc() = R"pbdoc(
        Bindings to the cpp code for TensorDB
        -------------------------------------
    )pbdoc";

  m.def(
      "set_spdlog_level", [](const std::string &level) { spdlog::set_level(spdlog::level::from_str(level)); },
      "Set spd log level. Supported levels are: trace, debug, info, warn, error, critical, off.");
}
