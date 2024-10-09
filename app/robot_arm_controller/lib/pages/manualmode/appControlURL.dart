class AppControlURL {
  static String baseURL = 'http://192.168.0.11:8000';

  static String requestStop = '$baseURL/move_motor/11/stop';
  static String requestLeft = '$baseURL/move_motor/11/cw';
  static String requestRight = '$baseURL/move_motor/11/ccw';
  static String requestUp = '$baseURL/move_motor/13/cw';
  static String requestDown = '$baseURL/move_motor/13/cw';

}