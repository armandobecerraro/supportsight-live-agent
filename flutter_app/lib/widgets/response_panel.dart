import 'package:flutter/material.dart';
import '../models/agent_response.dart';
import '../services/api_service.dart';

class ResponsePanel extends StatelessWidget {
  final AgentResponse? response;
  final bool loading;
  final ApiService api;
  const ResponsePanel({super.key, this.response, required this.loading, required this.api});

  @override
  Widget build(BuildContext context) {
    if (loading) return const Center(child: CircularProgressIndicator(color: Color(0xFF4F98A3)));
    if (response == null) return _card(const Column(children: [Text('🤖', style: TextStyle(fontSize: 40)), SizedBox(height: 8), Text('SupportSight will analyze your incident', style: TextStyle(color: Color(0xFF8B949E), fontSize: 14), textAlign: TextAlign.center)]));
    return SingleChildScrollView(child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
      _section('What I Understood', response!.whatIUnderstood, color: const Color(0xFF8B949E)),
      if (response!.whatISee != null) ...[const SizedBox(height: 12), _section('What I See', response!.whatISee!, color: const Color(0xFF4F98A3), borderColor: const Color(0xFF01696F))],
      if (response!.hypotheses.isNotEmpty) ...[const SizedBox(height: 12), _hypothesesCard()],
      if (response!.nextAction != null) ...[const SizedBox(height: 12), _section('Next Action', response!.nextAction!, color: const Color(0xFFF6AD55), borderColor: const Color(0xFFD69E2E))],
      if (response!.suggestedActions.isNotEmpty) ...[const SizedBox(height: 12), _actionsCard()],
    ]));
  }

  Widget _hypothesesCard() => _card(Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
    _label('Hypotheses'),
    const SizedBox(height: 12),
    ...response!.hypotheses.map((h) => Padding(padding: const EdgeInsets.only(bottom: 8), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Row(children: [Expanded(child: Text(h.description, style: const TextStyle(color: Colors.white, fontSize: 13))), Text('${(h.confidence * 100).toStringAsFixed(0)}%', style: const TextStyle(color: Color(0xFF4F98A3), fontSize: 12, fontFamily: 'monospace'))]),
      const SizedBox(height: 4),
      LinearProgressIndicator(value: h.confidence, backgroundColor: const Color(0xFF30363D), valueColor: const AlwaysStoppedAnimation<Color>(Color(0xFF01696F))),
    ]))),
  ]));

  Widget _actionsCard() => _card(Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
    _label('Suggested Actions'),
    const SizedBox(height: 12),
    ...response!.suggestedActions.map((a) => Container(margin: const EdgeInsets.only(bottom: 8), padding: const EdgeInsets.all(12), decoration: BoxDecoration(color: const Color(0xFF0D1117), borderRadius: BorderRadius.circular(8), border: Border.all(color: a.isDestructive ? Colors.red.shade800 : const Color(0xFF30363D))), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Text(a.title, style: const TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.w600)),
      const SizedBox(height: 4),
      Text(a.description, style: const TextStyle(color: Color(0xFF8B949E), fontSize: 12)),
    ]))),
  ]));

  Widget _section(String title, String content, {Color color = Colors.white, Color? borderColor}) => Container(padding: const EdgeInsets.all(14), decoration: BoxDecoration(color: const Color(0xFF161B22), borderRadius: BorderRadius.circular(12), border: Border.all(color: borderColor ?? const Color(0xFF30363D))), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [_label(title, color: color), const SizedBox(height: 6), Text(content, style: const TextStyle(color: Color(0xFFE1E4E8), fontSize: 13))]));
  Widget _card(Widget child) => Container(padding: const EdgeInsets.all(16), decoration: BoxDecoration(color: const Color(0xFF161B22), borderRadius: BorderRadius.circular(12), border: Border.all(color: const Color(0xFF30363D))), child: child);
  Widget _label(String text, {Color color = const Color(0xFF8B949E)}) => Text(text.toUpperCase(), style: TextStyle(color: color, fontSize: 10, fontWeight: FontWeight.w700, letterSpacing: 1.0));
}
