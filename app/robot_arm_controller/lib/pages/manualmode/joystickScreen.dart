import 'package:flutter/material.dart';
import 'package:robot_arm_controller/pages/manualmode/joystick.dart';
import 'package:robot_arm_controller/pages/manualmode/joystickRotation90.dart';

class JoystickScreen extends StatefulWidget {
  final String baseUrl;
  const JoystickScreen({super.key, required this.baseUrl});

  @override
  State<JoystickScreen> createState() => _JoystickScreenState();
}

class _JoystickScreenState extends State<JoystickScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey.shade100,
      appBar: AppBar(),
      body: LayoutBuilder(
        builder: (BuildContext context, BoxConstraints constraints) {
          if (constraints.maxWidth < constraints.maxHeight) {
            return BasicJoystick(baseURL: widget.baseUrl,);
          } else {
            return BasicJoystickRotation(baseURL: widget.baseUrl);
          }
        }
      ),
    );
  }
}
