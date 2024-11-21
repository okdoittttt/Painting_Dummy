import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:robot_arm_controller/pages/manualmode/appControlURL.dart';
import 'package:robot_arm_controller/pages/manualmode/joystick.dart';
import 'package:robot_arm_controller/pages/manualmode/joystickRotation90.dart';
import 'package:robot_arm_controller/pages/manualmode/squareJoystick.dart';

const ballSize = 20.0;
const step = 10.0;

class ManualMode extends StatelessWidget {
  final String baseURL;

  const ManualMode({super.key, required this.baseURL});

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
                return BasicJoystick(baseURL: baseURL,);
              } else {
                return BasicJoystickRotation(baseURL: baseURL,);
              }
            }
        ),
        // body: SquareJoystick(),
      ),
    );
  }
}
