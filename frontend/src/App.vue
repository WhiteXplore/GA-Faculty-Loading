<template>
  <div class="font-roboto"><router-view></router-view></div>
</template>

<style>
/* Scrollbar styling */
section::-webkit-scrollbar {
  width: 8px;
}
section::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.25);
  border-radius: 10px;
}
/* Elegant Glass Green Scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(0, 128, 0, 0.05); /* faint green track */
  border-radius: 10px;
  backdrop-filter: blur(4px);
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(
    180deg,
    rgba(34, 197, 94, 0.4) 0%,
    rgba(21, 128, 61, 0.6) 100%
  );
  border-radius: 10px;
  box-shadow: inset 0 0 4px rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(6px);
  transition: all 0.3s ease;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(
    180deg,
    rgba(34, 197, 94, 0.6) 0%,
    rgba(21, 128, 61, 0.8) 100%
  );
  box-shadow: inset 0 0 6px rgba(255, 255, 255, 0.4);
}
</style>
