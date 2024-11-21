import 'package:flutter/cupertino.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';

class BaseUrlProvider extends ChangeNotifier {
  String _baseUrl = 'http://172.20.10.6:8000';

  String get baseUrl => _baseUrl;

  set baseUrl(String newUrl) {
    _baseUrl = newUrl;
    notifyListeners();
    _saveBaseUrl(newUrl);
  }

  Future<void> _saveBaseUrl(String baseUrl) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.setString('baseUrl', baseUrl);
  }

  Future<void> loadBaseUrl() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    String? storedBaseUrl = prefs.getString('baseUrl');

    if (storedBaseUrl != null) {
      _baseUrl = storedBaseUrl;
    }
  }
}

class AppControlURL {
  // static String baseURL = 'http://192.168.0.11:8000';
  // static String baseURL = 'http://222.96.226.78:8000'; // 홍준
  // static String baseURL = 'http://192.168.56.145:8000'; // 재호
  // static String baseURL = 'http://172.20.10.6:8000'; // 옥무
  // static String baseURL(BuildContext context) => Provider.of<BaseUrlProvider>(context, listen: false).baseUrl;

  // 조이스틱 동작
  // String requestLeft = 'http://${Provider.of<BaseUrlProvider>(context as BuildContext, listen: false).baseUrl}/move_motor/11/cw';
  static String requestLeft = '/move_motor/11/cw';
  static String requestRight = '/move_motor/11/ccw';
  static String requestUp = '/move_height_motors/ccw/cw';
  static String requestDown = '/move_height_motors/cw/ccw';

  // 전후진
  static String requestGO = '/move_dual_motors/cw/ccw';
  static String requestBack = '/move_dual_motors/ccw/cw';

  // 멈춤 동작
  static String requestStop = '/move_motor/11/stop';
  static String requestHeight = '/move_height_motors/stop/stop';
  static String requestBackAndForth = '/move_dual_motors/stop/stop';

  // 페인트 분사
  static String sprayOn = '/paint/on';
  static String sprayOff = '/paint/off';
}