import 'package:flutter/material.dart';
import 'package:robot_arm_controller/pages/manualmode/joystick.dart';

class JoystickScreen extends StatefulWidget {
  const JoystickScreen({super.key});

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
            return BasicJoystick();
          } else {
            return BasicJoystick();
          }
        }
      ),
    );
  }
}
