import 'package:flutter/material.dart';

class InputPanel extends StatelessWidget {
  final TextEditingController descController, logsController;
  final bool loading;
  final VoidCallback onAnalyze;
  final String? error;
  const InputPanel({super.key, required this.descController, required this.logsController, required this.loading, required this.onAnalyze, this.error});

  @override
  Widget build(BuildContext context) {
    return Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
      _card(Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        _label('Incident Description'),
        const SizedBox(height: 8),
        TextField(controller: descController, maxLines: 4, style: const TextStyle(color: Colors.white, fontSize: 14),
          decoration: InputDecoration(hintText: 'Describe the incident...', hintStyle: const TextStyle(color: Color(0xFF6B7280)), filled: true, fillColor: const Color(0xFF161B22), border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: const BorderSide(color: Color(0xFF30363D))), enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: const BorderSide(color: Color(0xFF30363D))), focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: const BorderSide(color: Color(0xFF01696F))))),
      ])),
      const SizedBox(height: 12),
      _card(Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        _label('Paste Logs (optional)'),
        const SizedBox(height: 8),
        TextField(controller: logsController, maxLines: 6, style: const TextStyle(color: Colors.white, fontSize: 12, fontFamily: 'monospace'),
          decoration: InputDecoration(hintText: 'Paste log lines...', hintStyle: const TextStyle(color: Color(0xFF6B7280)), filled: true, fillColor: const Color(0xFF161B22), border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: const BorderSide(color: Color(0xFF30363D))), enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: const BorderSide(color: Color(0xFF30363D))), focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: const BorderSide(color: Color(0xFF01696F))))),
      ])),
      const SizedBox(height: 16),
      ElevatedButton(onPressed: loading ? null : onAnalyze,
        style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF01696F), foregroundColor: Colors.white, padding: const EdgeInsets.symmetric(vertical: 16), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))),
        child: loading ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2)) : const Text('Analyze Incident', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold))),
      if (error != null) ...[const SizedBox(height: 12), Container(padding: const EdgeInsets.all(12), decoration: BoxDecoration(color: const Color(0xFF3F1010), borderRadius: BorderRadius.circular(8), border: Border.all(color: Colors.red.shade800)), child: Text(error!, style: const TextStyle(color: Color(0xFFFC8181), fontSize: 12)))],
    ]);
  }

  Widget _card(Widget child) => Container(padding: const EdgeInsets.all(16), decoration: BoxDecoration(color: const Color(0xFF161B22), borderRadius: BorderRadius.circular(12), border: Border.all(color: const Color(0xFF30363D))), child: child);
  Widget _label(String text) => Text(text, style: const TextStyle(color: Color(0xFF8B949E), fontSize: 11, fontWeight: FontWeight.w600, letterSpacing: 0.8));
}
