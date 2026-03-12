'use client';

import { useState, useCallback } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { AgentResponse, SessionStatus } from '@/types';
import { analyzeIssue, confirmAction } from '@/services/api';
import { useAudioRecorder } from '@/hooks/useAudioRecorder';
import { useScreenCapture } from '@/hooks/useScreenCapture';

export default function Home() {
  const [description, setDescription] = useState('');
  const [logs, setLogs] = useState('');
  const [sessionId] = useState(uuidv4());
  const [status, setStatus] = useState<SessionStatus>('idle');
  const [response, setResponse] = useState<AgentResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const { isRecording, transcript, startRecording, stopRecording, clearTranscript } = useAudioRecorder();
  const { capturedImage, captureScreen, clearCapture } = useScreenCapture();

  const handleAnalyze = useCallback(async () => {
    const text = description || transcript;
    if (!text.trim()) return;
    setStatus('loading');
    setError(null);
    try {
      const result = await analyzeIssue({
        description: text,
        logs: logs || undefined,
        image_base64: capturedImage || undefined,
        session_id: sessionId,
      });
      setResponse(result);
      setStatus('active');
    } catch (e: any) {
      setError(e?.response?.data?.error || 'Failed to connect to agent');
      setStatus('error');
    }
  }, [description, transcript, logs, capturedImage, sessionId]);

  const handleConfirm = async (actionId: string, approved: boolean) => {
    if (!response) return;
    await confirmAction(response.session_id, actionId, approved);
    setResponse(prev => prev ? {
      ...prev,
      suggested_actions: prev.suggested_actions.map(a =>
        a.id === actionId ? { ...a, title: approved ? `✓ ${a.title}` : `✗ ${a.title}` } : a
      )
    } : prev);
  };

  return (
    <main className="max-w-6xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8 border-b border-gray-800 pb-6">
        <h1 className="text-3xl font-bold text-white">SupportSight <span className="text-[#4F98A3]">Live</span></h1>
        <p className="text-gray-400 mt-1">Multimodal incident support agent · Powered by Gemini Live API</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* LEFT: Input Panel */}
        <div className="space-y-4">
          {/* Voice */}
          <div className="bg-gray-900 rounded-xl p-4 border border-gray-800">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">Voice Input</h2>
              <button
                onClick={isRecording ? stopRecording : startRecording}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  isRecording
                    ? 'bg-red-600 hover:bg-red-700 text-white animate-pulse'
                    : 'bg-[#01696F] hover:bg-[#0C4E54] text-white'
                }`}
              >
                {isRecording ? '⏹ Stop Recording' : '🎤 Start Recording'}
              </button>
            </div>
            {transcript && (
              <div className="bg-gray-800 rounded-lg p-3 text-sm text-gray-200">
                <p>{transcript}</p>
                <button onClick={clearTranscript} className="text-xs text-gray-500 mt-2 hover:text-gray-300">Clear</button>
              </div>
            )}
          </div>

          {/* Text Description */}
          <div className="bg-gray-900 rounded-xl p-4 border border-gray-800">
            <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider mb-3">Incident Description</h2>
            <textarea
              value={description}
              onChange={e => setDescription(e.target.value)}
              placeholder="Describe the incident... e.g. 'API returning 503, high error rate in logs since 10:45am'"
              className="w-full bg-gray-800 text-gray-100 rounded-lg p-3 text-sm resize-none border border-gray-700 focus:border-[#01696F] focus:outline-none"
              rows={4}
            />
          </div>

          {/* Screen Capture */}
          <div className="bg-gray-900 rounded-xl p-4 border border-gray-800">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">Screen Evidence</h2>
              <button
                onClick={captureScreen}
                className="px-4 py-2 rounded-lg text-sm font-medium bg-gray-700 hover:bg-gray-600 text-white transition-all"
              >
                📸 Capture Screen
              </button>
            </div>
            {capturedImage && (
              <div className="relative">
                <img src={`data:image/png;base64,${capturedImage}`} alt="Captured screen" className="w-full rounded-lg border border-gray-700" />
                <button onClick={clearCapture} className="absolute top-2 right-2 bg-red-600 text-white text-xs px-2 py-1 rounded">✕</button>
              </div>
            )}
          </div>

          {/* Logs */}
          <div className="bg-gray-900 rounded-xl p-4 border border-gray-800">
            <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider mb-3">Paste Logs (optional)</h2>
            <textarea
              value={logs}
              onChange={e => setLogs(e.target.value)}
              placeholder="Paste log lines here..."
              className="w-full bg-gray-800 text-gray-100 rounded-lg p-3 text-xs font-mono resize-none border border-gray-700 focus:border-[#01696F] focus:outline-none"
              rows={5}
            />
          </div>

          {/* Analyze button */}
          <button
            onClick={handleAnalyze}
            disabled={status === 'loading'}
            className="w-full py-3 rounded-xl font-semibold text-white bg-[#01696F] hover:bg-[#0C4E54] disabled:opacity-50 disabled:cursor-not-allowed transition-all text-base"
          >
            {status === 'loading' ? '🔍 Analyzing...' : '🚀 Analyze Incident'}
          </button>

          {error && <div className="bg-red-900/40 border border-red-700 rounded-lg p-3 text-red-300 text-sm">{error}</div>}
        </div>

        {/* RIGHT: Agent Response Panel */}
        <div className="space-y-4">
          {!response && status !== 'loading' && (
            <div className="bg-gray-900 rounded-xl p-8 border border-gray-800 text-center text-gray-500">
              <div className="text-4xl mb-3">🤖</div>
              <p className="text-sm">SupportSight will analyze your incident using voice, visual context, and logs.</p>
            </div>
          )}

          {status === 'loading' && (
            <div className="bg-gray-900 rounded-xl p-8 border border-gray-800 text-center">
              <div className="animate-spin text-4xl mb-3">⚙️</div>
              <p className="text-gray-400 text-sm">Analyzing with Gemini...</p>
            </div>
          )}

          {response && (
            <>
              {/* What I Understood */}
              <div className="bg-gray-900 rounded-xl p-4 border border-gray-800">
                <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">What I Understood</h3>
                <p className="text-gray-200 text-sm">{response.what_i_understood}</p>
              </div>

              {/* What I See */}
              {response.what_i_see && (
                <div className="bg-gray-900 rounded-xl p-4 border border-[#01696F]/50">
                  <h3 className="text-xs font-semibold text-[#4F98A3] uppercase tracking-wider mb-2">What I See</h3>
                  <p className="text-gray-200 text-sm">{response.what_i_see}</p>
                </div>
              )}

              {/* Hypotheses */}
              {response.hypotheses.length > 0 && (
                <div className="bg-gray-900 rounded-xl p-4 border border-gray-800">
                  <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">Hypotheses</h3>
                  <div className="space-y-3">
                    {response.hypotheses.map((h, i) => (
                      <div key={i} className="bg-gray-800 rounded-lg p-3">
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-gray-200 text-sm">{h.description}</span>
                          <span className="text-xs text-[#4F98A3] font-mono ml-2 shrink-0">{(h.confidence * 100).toFixed(0)}%</span>
                        </div>
                        <div className="confidence-bar w-full" style={{ width: `${h.confidence * 100}%`, maxWidth: '100%' }} />
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Next Action */}
              {response.next_action && (
                <div className="bg-gray-900 rounded-xl p-4 border border-yellow-600/30">
                  <h3 className="text-xs font-semibold text-yellow-500 uppercase tracking-wider mb-2">Next Action</h3>
                  <p className="text-gray-200 text-sm">{response.next_action}</p>
                </div>
              )}

              {/* Suggested Actions */}
              {response.suggested_actions.length > 0 && (
                <div className="bg-gray-900 rounded-xl p-4 border border-gray-800">
                  <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">Suggested Actions</h3>
                  <div className="space-y-2">
                    {response.suggested_actions.map((action) => (
                      <div key={action.id} className={`rounded-lg p-3 border ${action.is_destructive ? 'border-red-700/50 bg-red-900/20' : 'border-gray-700 bg-gray-800'}`}>
                        <div className="flex items-start justify-between gap-3">
                          <div>
                            <p className="text-gray-200 text-sm font-medium">{action.title}</p>
                            <p className="text-gray-400 text-xs mt-1">{action.description}</p>
                            {action.is_destructive && <span className="text-xs text-red-400 font-medium">⚠ Requires confirmation</span>}
                          </div>
                          <div className="flex gap-2 shrink-0">
                            <button onClick={() => handleConfirm(action.id, true)} className="px-3 py-1 text-xs bg-[#01696F] hover:bg-[#0C4E54] text-white rounded-lg">Approve</button>
                            <button onClick={() => handleConfirm(action.id, false)} className="px-3 py-1 text-xs bg-gray-700 hover:bg-gray-600 text-white rounded-lg">Skip</button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {response.needs_more_info && (
                <div className="bg-yellow-900/20 border border-yellow-700/50 rounded-xl p-3 text-yellow-300 text-sm">
                  ℹ️ Provide logs or a screenshot for a more accurate analysis.
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </main>
  );
}
