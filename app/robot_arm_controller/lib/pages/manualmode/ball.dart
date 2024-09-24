import 'package:flutter/material.dart';
import 'package:robot_arm_controller/pages/manualmode/ballProperties.dart';

class Ball extends StatelessWidget {
  final double x;
  final double y;

  const Ball(this.x, this.y, {super.key});

  @override
  Widget build(BuildContext context) {
    BallProperties properties = BallProperties();
    return Positioned(
      left: x,
      top: y,
      child: Container(
        width: properties.ballSize,
        height: properties.ballSize,
        decoration: const BoxDecoration(
          shape: BoxShape.circle,
          color: Colors.redAccent,
          boxShadow: [
            BoxShadow(
              color: Colors.black12,
              spreadRadius: 2,
              blurRadius: 3,
              offset: Offset(0, 3),
            )
          ],
        ),
      ),
    );
  }
}
