import 'package:flutter/material.dart';
import 'package:robot_arm_controller/item/logoutButton.dart';
import 'package:robot_arm_controller/item/robotsList.dart';

class RobotsconnectionScreen extends StatefulWidget {
  const RobotsconnectionScreen({super.key});

  @override
  State<RobotsconnectionScreen> createState() => _RobotsconnectionScreenState();
}

class _RobotsconnectionScreenState extends State<RobotsconnectionScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.white,
        automaticallyImplyLeading: false,
        title: Text('Robot List'),
      ),
      backgroundColor: Colors.white,
      body: SingleChildScrollView( // 스크롤 가능한 영역을 만듭니다.
        child: Column(
          children: [
            Align(
              alignment: AlignmentDirectional.topEnd,
              child: Padding(
                padding: EdgeInsetsDirectional.fromSTEB(0, 20, 20, 0),
                child: LogoutButton(),
              ),
            ),
            RobotsList(),
            RobotsList(),
            RobotsList(),
          ],
        ),
      ),
    );

  }
}
