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

  Future<String> sendRequestStop(String baseUrl) async {
    try {
      final uriStop = Uri.parse('http://$baseUrl${AppControlURL.requestStop}');
      print(uriStop);
      final uriHeight = Uri.parse('http://$baseUrl${AppControlURL.requestHeight}');
      final uriBackAndForth = Uri.parse('http://$baseUrl${AppControlURL.requestBackAndForth}');
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

  Future<String> requestPaintOff(String baseUrl) async {
    try {
      final uriPaintOff = Uri.parse('http://$baseUrl${AppControlURL.sprayOff}');
      final response = await http.post(uriPaintOff);

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