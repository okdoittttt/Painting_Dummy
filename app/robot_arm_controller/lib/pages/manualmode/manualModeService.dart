import 'package:http/http.dart' as http;
import 'package:robot_arm_controller/pages/manualmode/appControlURL.dart';

class HttpService {
  final String url;

  HttpService(this.url);

  Future<String> sendRequest() async {
    try {
      final uri = Uri.parse(url);
      final response = await http.post(uri);
      if (response.statusCode == 200) {
        return '요청 성공!';
      } else {
        return '요청 실패: ${response.statusCode}';
      }
    } catch (e) {
      return '에러 발생: $e';
    }
  }

  Future<String> sendRequestStop() async {
    try {
      final uriStop = Uri.parse(AppControlURL.requestStop);
      final uriHeight = Uri.parse(AppControlURL.requestHeight);
      final uriBackAndForth = Uri.parse(AppControlURL.requestBackAndForth);
      final response = await http.post(uriStop);
      final responseHeight = await http.post(uriHeight);
      final responseBackAndForth = await http.post(uriBackAndForth);

      if (response.statusCode == 200) {
        return '요청 성공';
      } else {
        return '요청 실패: ${response.statusCode}';
      }
    } catch (e) {
      return '에러 발생: $e';
    }
  }
}