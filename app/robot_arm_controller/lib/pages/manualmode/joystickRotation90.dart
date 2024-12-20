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

class BasicJoystickRotation extends StatefulWidget {
  final String baseURL;

  const BasicJoystickRotation({super.key, required this.baseURL});

  @override
  State<BasicJoystickRotation> createState() => _JoystickExampleState();
}

class _JoystickExampleState extends State<BasicJoystickRotation> {
  // JoystickMode _joystickMode = JoystickMode.all;
  String _statusMessage = '자동 제어 시작';
  bool isPressedUpBtn = false;
  bool isPressedDownBtn = false;
  bool isPressedSprayBtn = false;

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
    print(url);
    setState(() {
      _statusMessage = '정지 중 ...';
    });

    final result = await httpService.sendRequestStop(widget.baseURL);
    setState(() {
      _statusMessage = result;
    });
  }

  Future<void> requestPainOff(String url) async {
    final HttpService httpService = HttpService(url);
    setState(() {
      _statusMessage = '정지 중 ...';
    });

    final result = await httpService.requestPaintOff(widget.baseURL);
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
                  GestureDetector(
                    onTapDown: (_) {
                      sendRequest('http://${widget.baseURL}${AppControlURL.requestUp}');
                      setState(() {
                        isPressedDownBtn = true;
                      });
                    },
                    onTapUp: (_) {
                      sendRequestStop('http://${widget.baseURL}${AppControlURL.requestStop}');
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
                      sendRequest('http://${widget.baseURL}${AppControlURL.sprayOn}');
                      setState(() {
                        isPressedSprayBtn = true;
                      });
                    },
                    onTapUp: (_) {
                      requestPainOff('http://${widget.baseURL}${AppControlURL.sprayOff}');
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
                      sendRequest('http://${widget.baseURL}${AppControlURL.requestDown}');
                      setState(() {
                        isPressedUpBtn = true;
                      });
                    },
                    onTapUp: (_) {
                      sendRequestStop('http://${widget.baseURL}${AppControlURL.requestStop}');
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
                  )
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
                        sendRequest('http://${widget.baseURL}${AppControlURL.requestBack}');
                      } else if (details.y < -0.5) {
                        sendRequest('http://${widget.baseURL}${AppControlURL.requestGO}');
                      } else if (details.x > 0.5) {
                        sendRequest('http://${widget.baseURL}${AppControlURL.requestRight}');
                      } else if (details.x < -0.5) {
                        sendRequest('http://${widget.baseURL}${AppControlURL.requestLeft}');
                      } else if (details.x == 0 || details.y == 0) {
                        sendRequestStop('http://${widget.baseURL}${AppControlURL.requestStop}');
                        sleep(Duration(milliseconds: 250));
                        sendRequestStop('http://${widget.baseURL}${AppControlURL.requestStop}');
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
