import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_joystick/flutter_joystick.dart';
import 'package:robot_arm_controller/pages/manualmode/appControlURL.dart';
import 'package:robot_arm_controller/pages/manualmode/ball.dart';
import 'package:robot_arm_controller/pages/manualmode/ballProperties.dart';
import 'package:robot_arm_controller/pages/manualmode/joysticModeDropdown.dart';

import 'manualModeService.dart';

BallProperties properties = BallProperties();

class BasicJoystickRotation extends StatefulWidget {
  const BasicJoystickRotation({super.key});

  @override
  State<BasicJoystickRotation> createState() => _JoystickExampleState();
}

class _JoystickExampleState extends State<BasicJoystickRotation> {
  // JoystickMode _joystickMode = JoystickMode.all;
  String _statusMessage = '자동 제어 시작';
  Future<void> sendRequest(String url) async {
    final HttpService httpService = HttpService(url);
    setState(() {
      _statusMessage = '정지 중 ...';
    });

    final result = await httpService.sendRequest();
    setState(() {
      // 전송에 성공한 경우 모달 혹은 알림 창을 출력하도록 변경 예정.
      _statusMessage = result;
    });
  }

  Future<void> sendRequestStop(String url) async {
    final HttpService httpService = HttpService(url);
    setState(() {
      _statusMessage = '정지 중 ...';
    });

    final result = await httpService.sendRequestStop();
    setState(() {
      _statusMessage = result;
    });
  }
  // =======================================================

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey.shade100,
      body: SafeArea(
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  ElevatedButton(
                      onPressed: () {
                        sendRequest(AppControlURL.requestUp);
                      },
                      style: ElevatedButton.styleFrom(
                          foregroundColor: Colors.white,
                          backgroundColor: Colors.orange,
                          minimumSize: Size(100, 50)),
                      child: Text('상승')),
                  ElevatedButton(
                      onPressed: () {
                        sendRequest(AppControlURL.requestDown);
                      },
                      style: ElevatedButton.styleFrom(
                          foregroundColor: Colors.white,
                          backgroundColor: Colors.orange,
                          minimumSize: Size(100, 50)),
                      child: Text('하강')),
                ],
              ),
            ),
            Column(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                Align(
                  alignment: const Alignment(0, 0.8),
                  child: Joystick(
                    mode: JoystickMode.horizontalAndVertical,
                    listener: (details) {
                      // 조이스틱 방향에 따른 동작
                      if (details.y > 0.5) {
                        sendRequest(AppControlURL.requestBack);
                      } else if (details.y < -0.5) {
                        sendRequest(AppControlURL.requestGO);
                      } else if (details.x > 0.5) {
                        sendRequest(AppControlURL.requestRight);
                      } else if (details.x < -0.5) {
                        sendRequest(AppControlURL.requestLeft);
                      } else if (details.x == 0 || details.y == 0) {
                        sendRequestStop(AppControlURL.requestStop);
                        sleep(Duration(milliseconds: 250));
                        sendRequestStop(AppControlURL.requestStop);
                      }
                    },
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
