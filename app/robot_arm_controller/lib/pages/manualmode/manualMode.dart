import 'package:flutter/material.dart';
import 'package:robot_arm_controller/pages/manualmode/joystick.dart';
import 'package:robot_arm_controller/pages/manualmode/joystickRotation90.dart';
import 'package:robot_arm_controller/pages/manualmode/squareJoystick.dart';

const ballSize = 20.0;
const step = 10.0;

class ManualMode extends StatelessWidget {
  const ManualMode({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('ROBOT CONTROLLER'),
        ),
        body: LayoutBuilder(
            builder: (BuildContext context, BoxConstraints constraints) {
              if (constraints.maxWidth < constraints.maxHeight) {
                return BasicJoystick();
              } else {
                return BasicJoystickRotation();
              }
            }
        ),
        // body: SquareJoystick(),
      ),
    );
  }
}
