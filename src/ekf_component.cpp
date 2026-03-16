#include <memory>
#include <vector>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "rclcpp_components/register_node_macro.hpp"
#include "robot_localization/ros_filter_types.hpp"

namespace robot_localization
{

/// Composable node wrapper for RosEkf.
///
/// Two adaptations are needed to run RosEkf inside a component container:
///
/// 1. RosFilter's constructor does Node(options.arguments()[0], options),
///    treating the first argument as the node name.  The standalone main()
///    sets arguments to {"ekf_filter_node"}, but the component container
///    populates arguments with ["--ros-args", …].  We prepend a default
///    node name so arguments()[0] is always valid; the __node:= remapping
///    from the launch file overrides it.
///
/// 2. RosFilter::initialize() calls shared_from_this(), which is unavailable
///    during construction.  A zero-delay wall timer defers the call until the
///    node is owned by a shared_ptr inside the component container's executor.
class RosEkfComponent : public RosEkf
{
  static rclcpp::NodeOptions prepend_node_name(rclcpp::NodeOptions options)
  {
    auto args = options.arguments();
    args.insert(args.begin(), "ekf_filter_node");
    return options.arguments(args);
  }

public:
  explicit RosEkfComponent(const rclcpp::NodeOptions & options)
  : RosEkf(prepend_node_name(options))
  {
    init_timer_ = this->create_wall_timer(
      std::chrono::milliseconds(0),
      [this]() {
        init_timer_->cancel();
        initialize();
      });
  }

private:
  rclcpp::TimerBase::SharedPtr init_timer_;
};

}  // namespace robot_localization

RCLCPP_COMPONENTS_REGISTER_NODE(robot_localization::RosEkfComponent)
