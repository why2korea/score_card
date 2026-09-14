/* ============================================================
   why2korea_scorecard 서비스워커 (sw.js)
   ------------------------------------------------------------
   역할: 앱 파일을 브라우저에 저장(캐시)해두어 필드에서 인터넷이
         약하거나 없어도 스코어 입력 화면(index.html)이 열리게 합니다.
         (지도 화면의 지도 타일/주소 검색은 인터넷이 필요합니다)

   ※ 코드를 수정했는데 휴대폰에서 바뀌지 않으면
      아래 CACHE_NAME 의 v1 을 v2, v3 ... 으로 올려주세요.
      그러면 옛 캐시를 버리고 새 파일을 내려받습니다.
   ============================================================ */

const CACHE_NAME = 'why2korea-scorecard-v13';

const PRECACHE_FILES = [
  './',
  './index.html',
  './manifest.json',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/apple-touch-icon.png'
];

// [1] 설치 시점: 위 파일들을 캐시에 담아둡니다
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => Promise.all(
        PRECACHE_FILES.map((url) => cache.add(url).catch(() => null))
      ))
      .then(() => self.skipWaiting())
  );
});

// [2] 활성화 시점: 이름이 다른(=옛 버전) 캐시를 모두 지웁니다
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((names) => Promise.all(
        names.filter((n) => n !== CACHE_NAME).map((n) => caches.delete(n))
      ))
      .then(() => self.clients.claim())
  );
});

// [3] 네트워크 요청 가로채기
self.addEventListener('fetch', (event) => {
  const request = event.request;

  if (request.method !== 'GET') return;

  // 같은 사이트의 파일만 다룹니다 (지도 타일·주소검색 요청은 그대로 통과)
  if (new URL(request.url).origin !== self.location.origin) return;

  // HTML 문서(앱 화면)는 '네트워크 먼저' → 수정한 코드가 바로 반영됩니다
  const isHtml = request.mode === 'navigate' ||
                 (request.headers.get('accept') || '').includes('text/html');

  if (isHtml) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          const copy = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, copy));
          return response;
        })
        .catch(() => caches.match(request).then((hit) => hit || caches.match('./index.html')))
    );
    return;
  }

  // 아이콘 등 나머지 파일은 '캐시 먼저' → 빠르게 열립니다
  event.respondWith(
    caches.match(request).then((hit) => hit || fetch(request).then((response) => {
      const copy = response.clone();
      caches.open(CACHE_NAME).then((cache) => cache.put(request, copy));
      return response;
    }).catch(() => hit))
  );
});
