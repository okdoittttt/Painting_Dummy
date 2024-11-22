import 'dart:ui';

import 'package:flutter/material.dart';
import 'package:robot_arm_controller/pages/manualmode/joystickScreen.dart';
import 'package:robot_arm_controller/pages/manualmode/manualMode.dart';
import 'package:robot_arm_controller/pages/robotList/robotsconnectionScreen.dart';
import '../manualmode/manualModeService.dart';

class AutoMode extends StatefulWidget {
  final String baseURL;

  const AutoMode({super.key, required this.baseURL});

  @override
  State<AutoMode> createState() => _AutoModeState();
}

class _AutoModeState extends State<AutoMode> {
  String robotsName = 'Open MANIPULATOR-X';
  String connectedState = '동작 비활성화 ...';
  bool buttonToggle = false;

  Future<void> sendRequestStop() async {
    final HttpService httpService = HttpService('http://${widget.baseURL}/initialize');
    setState(() {
      buttonToggle = false;
      connectedState = '동작 비활성화 ...';
    });

    final result = await httpService.sendRequest();
    setState(() {
    });
  }

  Future<void> sendRequest() async {
    final HttpService httpService = HttpService('http://${widget.baseURL}/initialize');
    setState(() {
      buttonToggle = true;
      connectedState = '동작 활성화 ...';
    });

    final result = await httpService.sendRequest();
    setState(() {
    });
  }

  // 모달 출력
  bool _showConfirmationDialog = false;

  void _showConfinationDialog() {
    setState(() {
      _showConfirmationDialog = true;
    });
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => FocusScope.of(context).unfocus(),
      child: Scaffold(
        backgroundColor: Colors.black,
        appBar: AppBar(
          backgroundColor: Colors.black,
        ),
        body: Align(
          alignment: AlignmentDirectional(0, 0),
          child: Column(
            mainAxisSize: MainAxisSize.max,
            children: [
              Row(
                mainAxisSize: MainAxisSize.max,
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Padding(
                    padding: EdgeInsetsDirectional.fromSTEB(16, 0, 16, 0),
                    child: Container(
                      width: 100,
                      height: 100,
                      decoration: BoxDecoration(
                        gradient: LinearGradient(
                          colors: [
                            Colors.orange,
                            Colors.black,
                          ],
                          stops: [0, 1],
                          begin: AlignmentDirectional(1, -1),
                          end: AlignmentDirectional(-1, 1),
                        ),
                        shape: BoxShape.circle,
                      ),
                      child: Align(
                        alignment: AlignmentDirectional(0, 0),
                        child: Padding(
                          padding: EdgeInsets.all(4),
                          child: Container(
                            width: 100,
                            height: 100,
                            decoration: BoxDecoration(
                              color: Colors.orange,
                              shape: BoxShape.circle,
                            ),
                            child: Padding(
                              padding: EdgeInsets.all(4),
                              child: ClipRRect(
                                borderRadius: BorderRadius.circular(50),
                                child: Image.asset(
                                  'assets/openmani.jpg',
                                  width: 100,
                                  height: 100,
                                  fit: BoxFit.cover,
                                ),
                              ),
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
              Padding(
                padding: EdgeInsetsDirectional.fromSTEB(0, 16, 0, 0),
                child: Text(
                  robotsName,
                  textAlign: TextAlign.center,
                  style: TextStyle(color: Colors.orange, fontSize: 25),
                ),
              ),
              Padding(
                padding: EdgeInsetsDirectional.fromSTEB(16, 4, 16, 0),
                child: Text(
                  connectedState,
                  style: TextStyle(
                      color: Colors.orange,
                      fontWeight: FontWeight.bold,
                      fontSize: 15),
                ),
              ),
              Expanded(
                child: Padding(
                  padding: EdgeInsetsDirectional.fromSTEB(0, 44, 0, 0),
                  child: Container(
                    width: double.infinity,
                    height: 400,
                    decoration: BoxDecoration(
                      color: Colors.white,
                      boxShadow: [
                        BoxShadow(
                          blurRadius: 3,
                          color: Color(0x33000000),
                          offset: Offset(
                            0,
                            -1,
                          ),
                        )
                      ],
                      borderRadius: BorderRadius.only(
                        bottomLeft: Radius.circular(0),
                        bottomRight: Radius.circular(0),
                        topLeft: Radius.circular(16),
                        topRight: Radius.circular(16),
                      ),
                    ),
                    child: SingleChildScrollView(
                      child: Column(
                        mainAxisSize: MainAxisSize.max,
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Padding(
                            padding: EdgeInsets.all(16),
                            child: Column(
                              mainAxisSize: MainAxisSize.max,
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  'Select Function',
                                  style: TextStyle(
                                      color: Colors.black, fontSize: 18),
                                ),
                                Align(
                                  alignment: AlignmentDirectional(0, 0),
                                  child: Padding(
                                    padding: EdgeInsetsDirectional.fromSTEB(
                                        0, 16, 0, 0),
                                    child: Wrap(
                                      spacing: 16,
                                      runSpacing: 16,
                                      alignment: WrapAlignment.start,
                                      crossAxisAlignment:
                                          WrapCrossAlignment.start,
                                      direction: Axis.horizontal,
                                      runAlignment: WrapAlignment.start,
                                      verticalDirection: VerticalDirection.down,
                                      clipBehavior: Clip.none,
                                      children: [
                                        // 자동 제어 모드 구현 후 사용
                                        GestureDetector(
                                          onTap: buttonToggle
                                              ? null
                                              : () => sendRequest(),
                                          child: Stack(children: [
                                            Container(
                                              width: MediaQuery.sizeOf(context)
                                                      .width *
                                                  0.4,
                                              height: 160,
                                              decoration: BoxDecoration(
                                                color: Color.fromARGB(
                                                    100, 196, 196, 196),
                                                borderRadius:
                                                    BorderRadius.circular(24),
                                              ),
                                              child: Padding(
                                                padding: EdgeInsets.all(12),
                                                child: Column(
                                                  mainAxisSize:
                                                      MainAxisSize.max,
                                                  mainAxisAlignment:
                                                      MainAxisAlignment.center,
                                                  children: [
                                                    Icon(
                                                      Icons.brightness_high,
                                                      color: Colors.orange,
                                                      size: 44,
                                                    ),
                                                    Padding(
                                                      padding:
                                                          EdgeInsetsDirectional
                                                              .fromSTEB(
                                                                  0, 12, 0, 4),
                                                      child: Text(
                                                        '자동 제어 시작',
                                                        textAlign:
                                                            TextAlign.center,
                                                        style: TextStyle(
                                                            color: Colors.black,
                                                            fontSize: 18),
                                                      ),
                                                    ),
                                                  ],
                                                ),
                                              ),
                                            ),
                                            if (buttonToggle)
                                              Positioned.fill(
                                                child: Opacity(
                                                  opacity: 0.8,
                                                  child: Container(
                                                    color: Colors.white
                                                        .withOpacity(0.8),
                                                  ),
                                                ),
                                              ),
                                          ]),
                                        ),
                                        GestureDetector(
                                          onTap: !buttonToggle
                                              ? null
                                              : () => sendRequestStop(),
                                          child: Stack(children: [
                                            Container(
                                              width: MediaQuery.sizeOf(context)
                                                      .width *
                                                  0.4,
                                              height: 160,
                                              decoration: BoxDecoration(
                                                color: Color.fromARGB(
                                                    100, 196, 196, 196),
                                                borderRadius:
                                                    BorderRadius.circular(24),
                                              ),
                                              child: Padding(
                                                padding: EdgeInsets.all(12),
                                                child: Column(
                                                  mainAxisSize:
                                                      MainAxisSize.max,
                                                  mainAxisAlignment:
                                                      MainAxisAlignment.center,
                                                  children: [
                                                    Icon(
                                                      Icons.brightness_low,
                                                      color: Colors.orange,
                                                      size: 44,
                                                    ),
                                                    Padding(
                                                      padding:
                                                          EdgeInsetsDirectional
                                                              .fromSTEB(
                                                                  0, 12, 0, 4),
                                                      child: Text(
                                                        '동작 초기화',
                                                        textAlign:
                                                            TextAlign.center,
                                                        style: TextStyle(
                                                          fontFamily:
                                                              'Urbanist',
                                                          letterSpacing: 0.0,
                                                          color: Colors.black,
                                                          fontSize: 18,
                                                        ),
                                                      ),
                                                    ),
                                                  ],
                                                ),
                                              ),
                                            ),
                                            if (!buttonToggle)
                                              Positioned.fill(
                                                child: Opacity(
                                                  opacity: 0.8,
                                                  child: Container(
                                                    color: Colors.white
                                                        .withOpacity(0.8),
                                                  ),
                                                ),
                                              )
                                          ]),
                                        ),
                                        GestureDetector(
                                          onTap: _showConfinationDialog,
                                          child: Stack(children: [
                                            Container(
                                              width: MediaQuery.sizeOf(context)
                                                      .width *
                                                  0.4,
                                              height: 160,
                                              decoration: BoxDecoration(
                                                color: Color.fromARGB(
                                                    100, 196, 196, 196),
                                                borderRadius:
                                                    BorderRadius.circular(24),
                                              ),
                                              child: Padding(
                                                padding: EdgeInsets.all(12),
                                                child: Column(
                                                  mainAxisSize:
                                                      MainAxisSize.max,
                                                  mainAxisAlignment:
                                                      MainAxisAlignment.center,
                                                  children: [
                                                    Icon(
                                                      Icons.do_not_disturb_alt,
                                                      color: Colors.orange,
                                                      size: 44,
                                                    ),
                                                    Padding(
                                                      padding:
                                                          EdgeInsetsDirectional
                                                              .fromSTEB(
                                                                  0, 12, 0, 4),
                                                      child: Text(
                                                        '연결 해제',
                                                        textAlign:
                                                            TextAlign.center,
                                                        style: TextStyle(
                                                          fontFamily:
                                                              'Urbanist',
                                                          letterSpacing: 0.0,
                                                          color: Colors.black,
                                                          fontSize: 18,
                                                        ),
                                                      ),
                                                    ),
                                                  ],
                                                ),
                                              ),
                                            ),
                                            if (buttonToggle)
                                              Positioned.fill(
                                                child: Opacity(
                                                  opacity: 0.8,
                                                  child: Container(
                                                    color: Colors.white
                                                        .withOpacity(0.8),
                                                  ),
                                                ),
                                              )
                                          ]),
                                        ),
                                        GestureDetector(
                                          onTap: () {
                                            Navigator.push(context, MaterialPageRoute(builder: (context) => ManualMode(baseURL: widget.baseURL)));
                                          },
                                          child: Stack(
                                            children: [
                                              Container(
                                                width:
                                                    MediaQuery.sizeOf(context)
                                                            .width *
                                                        0.4,
                                                height: 160,
                                                decoration: BoxDecoration(
                                                  color: Color.fromARGB(
                                                      100, 196, 196, 196),
                                                  borderRadius:
                                                      BorderRadius.circular(24),
                                                ),
                                                child: Padding(
                                                  padding: EdgeInsets.all(12),
                                                  child: Column(
                                                    mainAxisSize:
                                                        MainAxisSize.max,
                                                    mainAxisAlignment:
                                                        MainAxisAlignment
                                                            .center,
                                                    children: [
                                                      Icon(
                                                        Icons.model_training,
                                                        color: Colors.orange,
                                                        size: 44,
                                                      ),
                                                      Padding(
                                                        padding:
                                                            EdgeInsetsDirectional
                                                                .fromSTEB(0, 12,
                                                                    0, 4),
                                                        child: Text(
                                                          '수동 제어 변경',
                                                          textAlign:
                                                              TextAlign.center,
                                                          style: TextStyle(
                                                            fontFamily:
                                                                'Urbanist',
                                                            letterSpacing: 0.0,
                                                            color: Colors.black,
                                                            fontSize: 18,
                                                          ),
                                                        ),
                                                      ),
                                                    ],
                                                  ),
                                                ),
                                              ),
                                              if (buttonToggle)
                                                Positioned.fill(
                                                  child: Opacity(
                                                    opacity: 0.8,
                                                    child: Container(
                                                      color: Colors.white
                                                          .withOpacity(0.8),
                                                    ),
                                                  ),
                                                )
                                            ],
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
