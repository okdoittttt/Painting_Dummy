import 'package:flutter/material.dart';
import 'package:robot_arm_controller/pages/manualmode/joystick.dart';
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
        body: BasicJoystick(),
        // body: SquareJoystick(),
      ),
    );
  }
}
