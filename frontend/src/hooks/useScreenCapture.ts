import { useState, useCallback } from 'react';

export function useScreenCapture() {
  const [capturedImage, setCapturedImage] = useState<string | null>(null);

  const captureScreen = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getDisplayMedia({ video: true });
      const track = stream.getVideoTracks()[0];
      const imageCapture = new (window as any).ImageCapture(track);
      const bitmap = await imageCapture.grabFrame();
      const canvas = document.createElement('canvas');
      canvas.width = bitmap.width;
      canvas.height = bitmap.height;
      canvas.getContext('2d')?.drawImage(bitmap, 0, 0);
      const base64 = canvas.toDataURL('image/png').split(',')[1];
      setCapturedImage(base64);
      track.stop();
    } catch (e) {
      console.error('Screen capture failed:', e);
    }
  }, []);

  const clearCapture = useCallback(() => setCapturedImage(null), []);

  return { capturedImage, captureScreen, clearCapture };
}
