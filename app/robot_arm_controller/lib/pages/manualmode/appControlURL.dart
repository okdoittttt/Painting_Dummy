class AppControlURL {
  // static String baseURL = 'http://192.168.0.11:8000';
  static String baseURL = 'http://222.96.226.78:8000';

  // 조이스틱 동작
  static String requestLeft = '$baseURL/move_motor/11/cw';
  static String requestRight = '$baseURL/move_motor/11/ccw';
  static String requestUp = '$baseURL/move_height_motors/ccw/cw';
  static String requestDown = '$baseURL/move_height_motors/cw/ccw';

  // 전후진
  static String requestGO = '$baseURL/move_dual_motors/cw/ccw';
  static String requestBack = '$baseURL/move_dual_motors/ccw/cw';

  // 멈춤 동작
  static String requestStop = '$baseURL/move_motor/11/stop';
  static String requestHeight = '$baseURL/move_height_motors/stop/stop';
  static String requestBackAndForth = '$baseURL/move_dual_motors/stop/stop';
}