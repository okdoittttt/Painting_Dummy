import 'dart:async';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_joystick/flutter_joystick.dart';
import 'package:robot_arm_controller/pages/manualmode/appControlURL.dart';
import 'package:robot_arm_controller/pages/manualmode/ball.dart';
import 'package:robot_arm_controller/pages/manualmode/ballProperties.dart';
import 'package:robot_arm_controller/pages/manualmode/joysticModeDropdown.dart';

import 'manualModeService.dart';

BallProperties properties = BallProperties();

class BasicJoystick extends StatefulWidget {
  const BasicJoystick({super.key});

  @override
  State<BasicJoystick> createState() => _JoystickExampleState();
}

class _JoystickExampleState extends State<BasicJoystick> {
  // JoystickMode _joystickMode = JoystickMode.all;
  String _statusMessage = '자동 제어 시작';
  bool isPressedUpBtn = false;
  bool isPressedDownBtn = false;
  bool isPressedSprayBtn = false;

  // =======================================================
  // 움직임 동작 확인 테스트 코드
  // 조이스틱 움직임에 따른 함수 동작 예제 구현
  void moveUp() {
    print('Move Up');
  }

  void moveDown() {
    print('Move Down');
  }

  void moveLeft() {
    print('Move Left');
  }

  void moveRight() {
    print('Move Right');
  }

  void moveStop() {
    print('Move Stop');
  }

  void buttonDown() {
    print('Start');
  }

  void buttonUp() {
    print('End');
  }

  // =======================================================
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

  Future<void> requestPainOff(String url) async {
    final HttpService httpService = HttpService(url);
    setState(() {
      _statusMessage = '정지 중 ...';
    });

    final result = await httpService.requestPaintOff();
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
      appBar: AppBar(
          // 상하좌우만 동작하도록 구현, 만약 다른 방향 동작이 필요할 때 추석해제 하면 됨.
          // actions: [
          //   JoystickModeDropdown(
          //     mode: _joystickMode,
          //     onChanged: (JoystickMode value) {
          //       setState(() {
          //         _joystickMode = value;
          //       });
          //     },
          //   ),
          // ],
          ),
      body: SafeArea(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.end,
          children: [
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  GestureDetector(
                    onTapDown: (_) {
                      sendRequest(AppControlURL.requestUp);
                      setState(() {
                        isPressedDownBtn = true;
                      });
                    },
                    onTapUp: (_) {
                      sendRequestStop(AppControlURL.requestStop);
                      setState(() {
                        isPressedDownBtn = false;
                      });
                    },
                    child: Container(
                      width: 100,
                      height: 50,
                      decoration: BoxDecoration(
                          color: isPressedDownBtn ? Colors.blue : Colors.orange,
                          borderRadius: BorderRadius.circular(15),
                          boxShadow: [
                            BoxShadow(
                                color: Colors.grey.withOpacity(0.5),
                                spreadRadius: 2,
                                blurRadius: 5,
                                offset: Offset(0, 3))
                          ]),
                      child: Center(
                        child: Text(
                          '상승',
                          style: TextStyle(color: Colors.white),
                        ),
                      ),
                    ),
                  ),
                  GestureDetector(
                    onTapDown: (_) {
                      sendRequest(AppControlURL.sprayOn);
                      setState(() {
                        isPressedSprayBtn = true;
                      });
                    },
                    onTapUp: (_) {
                      requestPainOff(AppControlURL.sprayOff);
                      setState(() {
                        isPressedSprayBtn = false;
                      });
                    },
                    child: Container(
                      width: 150,
                      height: 70,
                      decoration: BoxDecoration(
                          color: isPressedSprayBtn ? Colors.blue : Colors.orange,
                          borderRadius: BorderRadius.circular(15),
                          boxShadow: [
                            BoxShadow(
                                color: Colors.grey.withOpacity(0.5),
                                spreadRadius: 2,
                                blurRadius: 5,
                                offset: Offset(0, 3))
                          ]),
                      child: Center(
                        child: Text(
                          '분사',
                          style: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold),
                        ),
                      ),
                    ),
                  ),
                  GestureDetector(
                    onTapDown: (_) {
                      sendRequest(AppControlURL.requestDown);
                      setState(() {
                        isPressedUpBtn = true;
                      });
                    },
                    onTapUp: (_) {
                      sendRequestStop(AppControlURL.requestStop);
                      setState(() {
                        isPressedUpBtn = false;
                      });
                    },
                    child: Container(
                      width: 100,
                      height: 50,
                      decoration: BoxDecoration(
                          color: isPressedUpBtn ? Colors.blue : Colors.orange,
                          borderRadius: BorderRadius.circular(15),
                          boxShadow: [
                            BoxShadow(
                                color: Colors.grey.withOpacity(0.5),
                                spreadRadius: 2,
                                blurRadius: 5,
                                offset: Offset(0, 3))
                          ]),
                      child: Center(
                        child: Text(
                          '하강',
                          style: TextStyle(color: Colors.white),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
            SizedBox(height: 30,),
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
                        moveDown();
                        sendRequest(AppControlURL.requestBack);
                      } else if (details.y < -0.5) {
                        moveUp();
                        sendRequest(AppControlURL.requestGO);
                      } else if (details.x > 0.5) {
                        moveRight();
                        sendRequest(AppControlURL.requestRight);
                      } else if (details.x < -0.5) {
                        moveLeft();
                        sendRequest(AppControlURL.requestLeft);
                      } else if (details.x == 0 || details.y == 0) {
                        moveStop();
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
