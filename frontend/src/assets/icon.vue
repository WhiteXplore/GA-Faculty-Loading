<template>
  <div>
    <!-- Material Icons  -->

    <svg
      v-if="name === 'dashboard'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 -950 920 900"
      stroke-width="35"
      stroke="currentColor"
      class="size-6"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M554.5-623v-136.5h205V-623h-205Zm-354 137v-273.5h205V-486h-205Zm354 285.5V-474h205v273.5h-205Zm-354 0V-337h205v136.5h-205Zm17.5-303h170V-742H218v238.5ZM572-218h170v-238.5H572V-218Zm0-421.5h170V-742H572v102.5ZM218-218h170v-101.5H218V-218Zm170-285.5Zm184-136Zm0 183Zm-184 137Z"
      />
    </svg>
    <svg
      v-if="name === 'class-list'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 -950 970 900"
      stroke-width="35"
      stroke="currentColor"
      class="size-7"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M316.5-317h232v-17.5h-232v17.5Zm0-154.5h327V-489h-327v17.5Zm0-154.5h327v-17.5h-327v17.5Zm-66.74 425.5q-20.9 0-35.08-14.18t-14.18-35.08v-460.48q0-20.9 14.18-35.08t35.08-14.18h460.48q20.9 0 35.08 14.18t14.18 35.08v460.48q0 20.9-14.18 35.08t-35.08 14.18H249.76ZM250-218h460q12 0 22-10t10-22v-460q0-12-10-22t-22-10H250q-12 0-22 10t-10 22v460q0 12 10 22t22 10Zm-32-524v524-524Z"
      />
    </svg>

    <svg
      v-if="name === 'set-up'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 -950 920 900"
      stroke-width="35"
      stroke="currentColor"
      class="size-7"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M249-396v-17.5h288v17.5H249Zm0-149v-17.5h430.5v17.5H249Zm0-148.5V-711h430.5v17.5H249ZM537.5-249v-66.5l199.48-198.48q2.78-2.93 5.63-3.73 2.85-.79 5.08-.79 2.45 0 5.37 1t5.44 2.5l44 46q1.85 3.18 3.18 5.84 1.32 2.66 1.32 5.17t-1.18 4.95q-1.17 2.44-3.34 5.06L604-249h-66.5Zm255-209-45-46 45 46Zm-240 194h44.76L736.5-402l-22.89-23-20.88-24L552.5-309v45Zm161-161-21-24 44 47-23-23Z"
      />
    </svg>

    <svg
      v-if="name === 'faculty-list'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 -950 970 900"
      stroke-width="35"
      stroke="currentColor"
      class="size-7"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M186.5-270.5v-29q0-17.42 8.02-27.32 8.03-9.9 23.95-18.78 40.03-23.9 83.28-39.65T418-401q73 0 116 15.75t83.71 39.66q15.79 9.09 23.79 18.92 8 9.83 8 27.17v29h-463Zm534.5 0V-291q0-29.5-6.2-52.23-6.19-22.73-13.3-36.27 9.5 8.5 21.97 16.4 12.47 7.89 29.03 17.6 8 4 14.75 19.83Q774-309.83 774-291v20.5h-53Zm-303-241q-37.79 0-63.39-25.61Q329-562.71 329-600.5t25.61-63.39q25.6-25.61 63.39-25.61t63.39 25.61Q507-638.29 507-600.5t-25.61 63.39Q455.79-511.5 418-511.5Zm185-89.31q0 37.39-25.61 63.1Q551.79-512 514-512q3.5 0 14.26 2.16 10.75 2.15 14.24 3.34 16.34-18.95 25.92-42.41 9.58-23.46 9.58-51.96 0-28.16-10.5-50.89-10.5-22.74-25-43.24-6.5 3-14 4.25T514-689.5q37.79 0 63.39 25.75Q603-638 603-600.81ZM204-288h428v-11.37q0-10.79-5.03-17.99-5.02-7.2-21.97-16.64-35.06-23-79.3-36.25-44.25-13.25-107.48-13.25-63.4 0-107.81 12.75Q266-358 231-334q-17.45 9.33-22.23 16.41-4.77 7.09-4.77 18V-288Zm214.15-241q29.85 0 50.6-20.9t20.75-50.75q0-29.85-20.9-50.6T417.85-672q-29.85 0-50.6 20.9t-20.75 50.75q0 29.85 20.9 50.6T418.15-529ZM418-288Zm0-312.5Z"
      />
    </svg>

    <svg
      v-if="name === 'faculty-loading'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 -950 970 900"
      stroke-width="35"
      stroke="currentColor"
      class="size-7"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M238.5-480.5q0 16 2.5 33.25t6.5 32.75q0 2.5-1.75 6t-5.75 3q-2.5-1-5.5-3T231-413q-5-15.5-7.5-32.5t-2.5-35q0-108.5 77-185T486.5-739H551l-77-77.5q-4-3.5-4.5-6t4.5-7.5q4.5-4.5 6.5-4.5t7 4.5l82 82.5q7.5 8 7.5 17.5t-7.5 17l-82 82q-4 4-6 4t-6.5-5q-5-4.5-5-6.5t5-7l76-76h-64.5q-105-2-176.5 69.25T238.5-480.5Zm483 0q0-16-2.5-32.75T713-546q0-3.5 1.75-6.5t5.75-4q2.5 0 4.25 1.5t2.75 3.5q4.5 17 8 34.5t3.5 36.5Q739-373 662-296t-188.5 74H409l77.5 77q3.5 4 4 6.5t-4 7q-5 5-7 5t-6.5-5L390.5-214q-7.5-7.5-7.5-17t8-17.5l82-82q3.5-3.5 6-4t7.5 4q4.5 5 4.5 7t-4.5 6.5L409-239.5h64.5q105 2 176.5-69.25t71.5-171.75Z"
      />
    </svg>
    <svg
      v-if="name === 'faculty-loading1'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 -950 920 900"
      stroke-width="35"
      stroke="currentColor"
      class="size-4"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M238.5-480.5q0 16 2.5 33.25t6.5 32.75q0 2.5-1.75 6t-5.75 3q-2.5-1-5.5-3T231-413q-5-15.5-7.5-32.5t-2.5-35q0-108.5 77-185T486.5-739H551l-77-77.5q-4-3.5-4.5-6t4.5-7.5q4.5-4.5 6.5-4.5t7 4.5l82 82.5q7.5 8 7.5 17.5t-7.5 17l-82 82q-4 4-6 4t-6.5-5q-5-4.5-5-6.5t5-7l76-76h-64.5q-105-2-176.5 69.25T238.5-480.5Zm483 0q0-16-2.5-32.75T713-546q0-3.5 1.75-6.5t5.75-4q2.5 0 4.25 1.5t2.75 3.5q4.5 17 8 34.5t3.5 36.5Q739-373 662-296t-188.5 74H409l77.5 77q3.5 4 4 6.5t-4 7q-5 5-7 5t-6.5-5L390.5-214q-7.5-7.5-7.5-17t8-17.5l82-82q3.5-3.5 6-4t7.5 4q4.5 5 4.5 7t-4.5 6.5L409-239.5h64.5q105 2 176.5-69.25t71.5-171.75Z"
      />
    </svg>

    <svg
      v-if="name === 'prospectus'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 -950 920 900"
      stroke-width="35"
      stroke="currentColor"
      class="size-6"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M351.83-480.83H609q4.31 0 7.74-3.42 3.43-3.41 3.43-8.33t-3.43-8.17Q613.31-504 609-504H351.83q-5.26 0-8.63 3.48-3.37 3.47-3.37 7.85 0 5.34 3.37 8.59t8.63 3.25Zm0 106.33H609q4.31 0 7.74-3 3.43-2.99 3.43-8.33t-3.43-8.59q-3.43-3.25-7.74-3.25H351.83q-5.26 0-8.63 3.42-3.37 3.41-3.37 8.75 0 5.33 3.37 8.17 3.37 2.83 8.63 2.83Zm0 107.17H489q4.31 0 7.74-3.42 3.43-3.41 3.43-8.33t-3.43-8.17q-3.43-3.25-7.74-3.25H351.83q-5.26 0-8.63 3.48-3.37 3.47-3.37 7.85 0 5.34 3.37 8.59t8.63 3.25Zm-83.36 133.66q-22.78 0-38.87-16.09-16.1-16.1-16.1-38.85v-582.78q0-22.75 16.1-38.85 16.09-16.09 39.07-16.09h298.66q11.9 0 21.87 4.58t18.42 11.51l122.26 122.65q7.79 8.42 12.2 18.28 4.42 9.87 4.42 21.64v458.84q0 22.97-16.1 39.07-16.09 16.09-38.87 16.09H268.47ZM723.33-659H620.67q-17.18 0-29.68-12.49-12.49-12.5-12.49-29.68v-102H268.67q-12 0-22 10t-10 22v582.34q0 12 10 22t22 10h422.66q12 0 22-10t10-22V-659ZM236.67-803.17V-659v-144.17 646.34-646.34Z"
      />
    </svg>
    <svg
      v-if="name === 'user-account'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 -950 920 900"
      stroke-width="35"
      stroke="currentColor"
      class="size-6"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M258.09-265.5Q312.5-300 365-316.5T480-333q62.5 0 115 16.5t107.5 51q41.5-41.5 64.25-96.15Q789.5-416.3 789.5-479.9q0-128.77-90.48-219.19-90.48-90.41-219.25-90.41-128.77 0-219.02 90.41-90.25 90.42-90.25 219.19 0 63.6 22.75 118.25t64.84 96.15ZM480.14-435Q431-435 397-468.86t-34-83Q363-601 396.86-635t83-34Q529-669 563-635.14t34 83Q597-503 563.14-469t-83 34Zm.14 282q-67.69 0-127.6-25.26-59.9-25.27-104.54-70Q203.5-293 178.25-352.8 153-412.59 153-480.71q0-68.2 25.26-127.36 25.27-59.15 70-103.79Q293-756.5 352.8-781.75 412.59-807 480.71-807q68.2 0 127.36 25.26 59.15 25.27 103.79 70Q756.5-667 781.75-607.73T807-480.28q0 67.69-25.26 127.6-25.27 59.9-70 104.54Q667-203.5 607.73-178.25T480.28-153Zm-.31-17.5q54.53 0 110.28-21.25T689-251q-44-29.5-96.72-47t-112.19-17.5q-59.47 0-113.78 16T271-251q43 38 98.72 59.25t110.25 21.25Zm.03-282q40.5 0 70-29.5t29.5-70q0-40.5-29.5-70t-70-29.5q-40.5 0-70 29.5t-29.5 70q0 40.5 29.5 70t70 29.5Zm0-99.5Zm0 304Z"
      />
    </svg>

    <svg
      v-if="name === 'summary'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 -950 920 900"
      stroke-width="35"
      stroke="currentColor"
      class="size-6"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M602.38-245.5q-98.35 0-166.62-68.26-68.26-68.27-68.26-166.62 0-97.12 68.26-165.87Q504.03-715 602.38-715q97.12 0 165.87 68.75T837-480.38q0 98.35-68.75 166.62-68.75 68.26-165.87 68.26Zm-.88-17.5q90.5 0 154.25-62.75T819.5-479.5q0-90.5-63.75-154.25T602-697.5q-91.5 0-154.25 63.75T385-480q0 91.5 62.75 154.25T601.5-263Zm9.56-219.59v-115.32q0-3.79-2.65-6.44-2.65-2.65-6.45-2.65-3.76 0-6.11 2.55-2.35 2.55-2.35 6.19v111.11q0 4.22.75 8.68.75 4.47 6.01 9.78l87.79 87.86q2.45 3.33 5.62 3.33 3.16 0 6.33-3.5 3-2.67 3-5.58 0-2.92-2.82-6.25l-89.12-89.76ZM192.26-627.5q-3.71 0-6.24-2.32-2.52-2.33-2.52-6 0-3.68 2.35-6.43 2.35-2.75 6.06-2.75h103.83q3.71 0 6.49 2.57 2.77 2.58 2.77 6.25 0 3.68-2.6 6.18-2.6 2.5-6.31 2.5H192.26ZM144-471.5q-3.75 0-6.12-2.32-2.38-2.33-2.38-6 0-3.68 2.38-6.43Q140.25-489 144-489h152q3.75 0 6.38 2.57 2.62 2.58 2.62 6.25 0 3.68-2.62 6.18-2.63 2.5-6.38 2.5H144Zm48.26 156q-3.71 0-6.24-2.32-2.52-2.33-2.52-6 0-3.68 2.35-6.43 2.35-2.75 6.06-2.75h103.83q3.71 0 6.49 2.57 2.77 2.58 2.77 6.25 0 3.68-2.6 6.18-2.6 2.5-6.31 2.5H192.26ZM602-480Z"
      />
    </svg>

    <svg
      v-if="name === 'expertise'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 -950 920 900"
      stroke-width="35"
      stroke="currentColor"
      class="size-7"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M259.5-362.5q-10.57-4.3-17.54-17.26-6.96-12.95-6.96-26.08v-143.78L174-578q-6.5-3.64-10.25-9.51-3.75-5.86-3.75-12.34 0-6.47 3.75-12.31Q167.5-618 174-622l247.65-119.69q4.93-2.81 10.5-3.56t10.97-.75q5.39 0 10.84 1 5.46 1 10.82 3.23L747-607.5q6 4.5 9.5 9.88 3.5 5.39 3.5 11.62v200q0 2.45-3.32 5.73-3.33 3.27-5.72 3.27-2.96 0-5.71-3.27-2.75-3.28-2.75-5.73v-207L651-549.52v143.71q0 13.1-6.46 25.55-6.47 12.46-18.04 17.76l-161.44 80.48q-5.56 3.02-11.07 3.52-5.52.5-10.8.5-5.28 0-10.98-.5-5.71-.5-11.27-3.52L259.5-362.5Zm171.5-109q7 4 12.5 4t12.5-4L711-600 456-727q-7-3.5-12.5-3.5T431-727L175.5-600 431-471.5ZM430-299q7 4 13 4t13-4l162.5-78.83q8-5 11.5-11.5t3.5-16.5V-540L467-458q-7 3.5-12.54 4.5-5.54 1-11.58 1-7.38 0-12.63-1-5.25-1-10.75-4.5l-167-82v134.17q0 8 3.5 15.5t11.5 12.5L430-299Zm14.5-160.5Zm-1.5 42Zm0 0Z"
      />
    </svg>

    <svg
      v-if="name === 'refresh'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 -950 920 900"
      stroke-width="35"
      stroke="currentColor"
      class="size-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M484.5-248.5q-96.73 0-164.36-67.59-67.64-67.59-67.64-163.75t67.64-163.91q67.63-67.75 164.36-67.75 67.5 0 121.5 34t84.5 89V-703q0-3.25 2.32-5.88 2.33-2.62 6-2.62 3.68 0 6.43 2.62Q708-706.25 708-703v109q0 10.55-7.22 17.78Q693.55-569 683-569H574q-3.75 0-6.12-2.57-2.38-2.58-2.38-6.25 0-3.18 2.38-5.93 2.37-2.75 6.12-2.75h94q-28-49-76.25-78.25T484.5-694q-89.5 0-152 62.5T270-480q0 89 62.5 151.5t152 62.5q79.01 0 139.25-50.75Q684-367.5 698.5-444.5q-2-5.5 1-10.25t7.34-6.25q4.66-.5 8.16 0t6.5 6q-12 89.5-79.25 148-67.26 58.5-157.75 58.5Z"
      />
    </svg>

    <svg
      v-if="name === 'upload'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 -950 920 900"
      stroke-width="35"
      stroke="currentColor"
      class="size-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M471.5-360.5V-727l-90 90-13-10.5L480-759l112 111.5-13 10.5-90-90v366.5h-17.5ZM298.08-249q-21.02 0-35.05-14.18Q249-277.36 249-298.43v-41.07h17.5v41q0 12 10 22t22 10h363q12 0 22-10t10-22v-41H711v41.07q0 21.07-14.19 35.25Q682.61-249 661.6-249H298.08Z"
      />
    </svg>

    <!-- Material Icons  -->
    <!-- Hero Icons  -->

    <svg
      v-if="name == 'uploads'"
      xmlns="http://www.w3.org/2000/svg"
      class="w-4 h-4"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
      />
    </svg>
    <svg
      v-if="name == 'circle-add'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-4"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
      />
    </svg>

    <svg
      v-if="name == 'circle-add1'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
      />
    </svg>

    <svg
      v-if="name == 'arrow-up'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="2.5"
      stroke="currentColor"
      class="size-4"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="m4.5 15.75 7.5-7.5 7.5 7.5"
      />
    </svg>
    <svg
      v-if="name == 'arrow-down'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="2.5"
      stroke="currentColor"
      class="size-4"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="m19.5 8.25-7.5 7.5-7.5-7.5"
      />
    </svg>
    <svg
      v-if="name == 'add-account'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
      />
    </svg>

    <svg
      v-if="name == 'add-account1'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-10 text-gray-400"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
      />
    </svg>
    <svg
      v-if="name == 'close'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="2.5"
      stroke="currentColor"
      class="size-4 hover:text-defaultGreen"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M6 18 18 6M6 6l12 12"
      />
    </svg>
    <svg
      v-if="name == 'logout'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-4"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M8.25 9V5.25A2.25 2.25 0 0 1 10.5 3h6a2.25 2.25 0 0 1 2.25 2.25v13.5A2.25 2.25 0 0 1 16.5 21h-6a2.25 2.25 0 0 1-2.25-2.25V15m-3 0-3-3m0 0 3-3m-3 3H15"
      />
    </svg>
    <svg
      v-if="name == 'next'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="m8.25 4.5 7.5 7.5-7.5 7.5"
      />
    </svg>
    <svg
      v-if="name == 'back'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M15.75 19.5 8.25 12l7.5-7.5"
      />
    </svg>
    <svg
      v-if="name == 'exclamation'"
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      class="w-8 h-9"
    >
      <text
        x="50%"
        y="50%"
        text-anchor="middle"
        dy=".3em"
        class="text-xl font-bold"
        fill="white"
      >
        !
      </text>
    </svg>
    <svg
      v-if="name == 'exclamation-circle'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z"
      />
    </svg>

    <!-- <svg
      v-if="name == 'dashboard'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-4"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M3.75 6A2.25 2.25 0 0 1 6 3.75h2.25A2.25 2.25 0 0 1 10.5 6v2.25a2.25 2.25 0 0 1-2.25 2.25H6a2.25 2.25 0 0 1-2.25-2.25V6ZM3.75 15.75A2.25 2.25 0 0 1 6 13.5h2.25a2.25 2.25 0 0 1 2.25 2.25V18a2.25 2.25 0 0 1-2.25 2.25H6A2.25 2.25 0 0 1 3.75 18v-2.25ZM13.5 6a2.25 2.25 0 0 1 2.25-2.25H18A2.25 2.25 0 0 1 20.25 6v2.25A2.25 2.25 0 0 1 18 10.5h-2.25a2.25 2.25 0 0 1-2.25-2.25V6ZM13.5 15.75a2.25 2.25 0 0 1 2.25-2.25H18a2.25 2.25 0 0 1 2.25 2.25V18A2.25 2.25 0 0 1 18 20.25h-2.25A2.25 2.25 0 0 1 13.5 18v-2.25Z"
      />
    </svg> -->
    <svg
      v-if="name == 'general'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-4"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z"
      />
    </svg>

    <svg
      v-if="name == 'lock'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M16.5 10.5V6.75a4.5 4.5 0 1 0-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H6.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25Z"
      />
    </svg>
    <svg
      v-if="name == 'non-print'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M6.72 13.829c-.24.03-.48.062-.72.096m.72-.096a42.415 42.415 0 0 1 10.56 0m-10.56 0L6.34 18m10.94-4.171c.24.03.48.062.72.096m-.72-.096L17.66 18m0 0 .229 2.523a1.125 1.125 0 0 1-1.12 1.227H7.231c-.662 0-1.18-.568-1.12-1.227L6.34 18m11.318 0h1.091A2.25 2.25 0 0 0 21 15.75V9.456c0-1.081-.768-2.015-1.837-2.175a48.055 48.055 0 0 0-1.913-.247M6.34 18H5.25A2.25 2.25 0 0 1 3 15.75V9.456c0-1.081.768-2.015 1.837-2.175a48.041 48.041 0 0 1 1.913-.247m10.5 0a48.536 48.536 0 0 0-10.5 0m10.5 0V3.375c0-.621-.504-1.125-1.125-1.125h-8.25c-.621 0-1.125.504-1.125 1.125v3.659M18 10.5h.008v.008H18V10.5Zm-3 0h.008v.008H15V10.5Z"
      />
    </svg>

    <svg
      v-if="name == 'request'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M10.125 2.25h-4.5c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125v-9M10.125 2.25h.375a9 9 0 0 1 9 9v.375M10.125 2.25A3.375 3.375 0 0 1 13.5 5.625v1.5c0 .621.504 1.125 1.125 1.125h1.5a3.375 3.375 0 0 1 3.375 3.375M9 15l2.25 2.25L15 12"
      />
    </svg>
    <svg
      v-if="name == 'utilities'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-4"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M6.429 9.75 2.25 12l4.179 2.25m0-4.5 5.571 3 5.571-3m-11.142 0L2.25 7.5 12 2.25l9.75 5.25-4.179 2.25m0 0L21.75 12l-4.179 2.25m0 0 4.179 2.25L12 21.75 2.25 16.5l4.179-2.25m11.142 0-5.571 3-5.571-3"
      />
    </svg>
    <svg
      v-if="name == 'users'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-4"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M15 19.128a9.38 9.38 0 0 0 2.625.372 9.337 9.337 0 0 0 4.121-.952 4.125 4.125 0 0 0-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 0 1 8.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0 1 11.964-3.07M12 6.375a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0Zm8.25 2.25a2.625 2.625 0 1 1-5.25 0 2.625 2.625 0 0 1 5.25 0Z"
      />
    </svg>

    <svg
      v-if="name == 'users1'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-6"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M15 19.128a9.38 9.38 0 0 0 2.625.372 9.337 9.337 0 0 0 4.121-.952 4.125 4.125 0 0 0-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 0 1 8.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0 1 11.964-3.07M12 6.375a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0Zm8.25 2.25a2.625 2.625 0 1 1-5.25 0 2.625 2.625 0 0 1 5.25 0Z"
      />
    </svg>
    <svg
      v-if="name == 'reports'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-4"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 0 1-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 0 1 1.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 0 0-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 0 1-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 0 0-3.375-3.375h-1.5a1.125 1.125 0 0 1-1.125-1.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H9.75"
      />
    </svg>

    <svg
      v-if="name == 'burger'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-6"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
      />
    </svg>
    <svg
      v-if="name == 'books'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M10.125 2.25h-4.5c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125v-9M10.125 2.25h.375a9 9 0 0 1 9 9v.375M10.125 2.25A3.375 3.375 0 0 1 13.5 5.625v1.5c0 .621.504 1.125 1.125 1.125h1.5a3.375 3.375 0 0 1 3.375 3.375M9 15l2.25 2.25L15 12"
      />
    </svg>
    <svg
      v-if="name == 'add'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M12 4.5v15m7.5-7.5h-15"
      />
    </svg>
    <svg
      v-if="name == 'import'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3"
      />
    </svg>
    <svg
      v-if="name == 'export'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-4"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5"
      />
    </svg>
    <svg
      v-if="name == 'add-docs'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m3.75 9v6m3-3H9m1.5-12H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z"
      />
    </svg>
    <svg
      v-if="name == 'edit'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10"
      />
    </svg>
    <svg
      v-if="name == 'delete'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-4"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"
      />
    </svg>
    <svg
      v-if="name == 'warning'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-14"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z"
      />
    </svg>
    <svg
      v-if="name == 'circle-check'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-4"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
      />
    </svg>

    <svg
      v-if="name == 'check'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-6"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
      />
    </svg>

    <svg
      v-if="name == 'minus'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-6"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M15 12H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
      />
    </svg>

    <svg
      v-if="name == 'check2'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-4"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
      />
    </svg>
    <svg
      v-if="name == 'question'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-12"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z"
      />
    </svg>
    <svg
      v-if="name == 'download'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="m9 13.5 3 3m0 0 3-3m-3 3v-6m1.06-4.19-2.12-2.12a1.5 1.5 0 0 0-1.061-.44H4.5A2.25 2.25 0 0 0 2.25 6v12a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9a2.25 2.25 0 0 0-2.25-2.25h-5.379a1.5 1.5 0 0 1-1.06-.44Z"
      />
    </svg>
    <svg
      v-if="name == 'download1'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="m9 12.75 3 3m0 0 3-3m-3 3v-7.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
      />
    </svg>
    <svg
      v-if="name == 'add-students'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M18 7.5v3m0 0v3m0-3h3m-3 0h-3m-2.25-4.125a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0ZM3 19.235v-.11a6.375 6.375 0 0 1 12.75 0v.109A12.318 12.318 0 0 1 9.374 21c-2.331 0-4.512-.645-6.374-1.766Z"
      />
    </svg>
    <svg
      v-if="name == 'transaction-logs'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-4"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M12 7.5h1.5m-1.5 3h1.5m-7.5 3h7.5m-7.5 3h7.5m3-9h3.375c.621 0 1.125.504 1.125 1.125V18a2.25 2.25 0 0 1-2.25 2.25M16.5 7.5V18a2.25 2.25 0 0 0 2.25 2.25M16.5 7.5V4.875c0-.621-.504-1.125-1.125-1.125H4.125C3.504 3.75 3 4.254 3 4.875V18a2.25 2.25 0 0 0 2.25 2.25h13.5M6 7.5h3v3H6v-3Z"
      />
    </svg>
    <svg
      v-if="name == 'eye'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z"
      />
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
      />
    </svg>

    <svg
      v-if="name == 'history'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M12 7.5h1.5m-1.5 3h1.5m-7.5 3h7.5m-7.5 3h7.5m3-9h3.375c.621 0 1.125.504 1.125 1.125V18a2.25 2.25 0 0 1-2.25 2.25M16.5 7.5V18a2.25 2.25 0 0 0 2.25 2.25M16.5 7.5V4.875c0-.621-.504-1.125-1.125-1.125H4.125C3.504 3.75 3 4.254 3 4.875V18a2.25 2.25 0 0 0 2.25 2.25h13.5M6 7.5h3v3H6v-3Z"
      />
    </svg>

    <svg
      v-if="name == 'printer'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M6.72 13.829c-.24.03-.48.062-.72.096m.72-.096a42.415 42.415 0 0 1 10.56 0m-10.56 0L6.34 18m10.94-4.171c.24.03.48.062.72.096m-.72-.096L17.66 18m0 0 .229 2.523a1.125 1.125 0 0 1-1.12 1.227H7.231c-.662 0-1.18-.568-1.12-1.227L6.34 18m11.318 0h1.091A2.25 2.25 0 0 0 21 15.75V9.456c0-1.081-.768-2.015-1.837-2.175a48.055 48.055 0 0 0-1.913-.247M6.34 18H5.25A2.25 2.25 0 0 1 3 15.75V9.456c0-1.081.768-2.015 1.837-2.175a48.041 48.041 0 0 1 1.913-.247m10.5 0a48.536 48.536 0 0 0-10.5 0m10.5 0V3.375c0-.621-.504-1.125-1.125-1.125h-8.25c-.621 0-1.125.504-1.125 1.125v3.659M18 10.5h.008v.008H18V10.5Zm-3 0h.008v.008H15V10.5Z"
      />
    </svg>
    <svg
      v-if="name == 'printer1'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-8"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M6.72 13.829c-.24.03-.48.062-.72.096m.72-.096a42.415 42.415 0 0 1 10.56 0m-10.56 0L6.34 18m10.94-4.171c.24.03.48.062.72.096m-.72-.096L17.66 18m0 0 .229 2.523a1.125 1.125 0 0 1-1.12 1.227H7.231c-.662 0-1.18-.568-1.12-1.227L6.34 18m11.318 0h1.091A2.25 2.25 0 0 0 21 15.75V9.456c0-1.081-.768-2.015-1.837-2.175a48.055 48.055 0 0 0-1.913-.247M6.34 18H5.25A2.25 2.25 0 0 1 3 15.75V9.456c0-1.081.768-2.015 1.837-2.175a48.041 48.041 0 0 1 1.913-.247m10.5 0a48.536 48.536 0 0 0-10.5 0m10.5 0V3.375c0-.621-.504-1.125-1.125-1.125h-8.25c-.621 0-1.125.504-1.125 1.125v3.659M18 10.5h.008v.008H18V10.5Zm-3 0h.008v.008H15V10.5Z"
      />
    </svg>
    <svg
      v-if="name == 'back1'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-6"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="m11.25 9-3 3m0 0 3 3m-3-3h7.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
      />
    </svg>
    <svg
      v-if="name == 'additional-requirements'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m3.75 9v6m3-3H9m1.5-12H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z"
      />
    </svg>
    <svg
      v-if="name == 'circle-close3'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-6"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
      />
    </svg>

    <svg
      v-if="name == 'circle-close'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
      />
    </svg>
    <svg
      v-if="name == 'circle-close2'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-4"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
      />
    </svg>
    <svg
      v-if="name == 'time'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
      />
    </svg>

    <svg
      v-if="name == 'setting'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-4"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.325.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 0 1 1.37.49l1.296 2.247a1.125 1.125 0 0 1-.26 1.431l-1.003.827c-.293.241-.438.613-.43.992a7.723 7.723 0 0 1 0 .255c-.008.378.137.75.43.991l1.004.827c.424.35.534.955.26 1.43l-1.298 2.247a1.125 1.125 0 0 1-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.47 6.47 0 0 1-.22.128c-.331.183-.581.495-.644.869l-.213 1.281c-.09.543-.56.94-1.11.94h-2.594c-.55 0-1.019-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 0 1-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 0 1-1.369-.49l-1.297-2.247a1.125 1.125 0 0 1 .26-1.431l1.004-.827c.292-.24.437-.613.43-.991a6.932 6.932 0 0 1 0-.255c.007-.38-.138-.751-.43-.992l-1.004-.827a1.125 1.125 0 0 1-.26-1.43l1.297-2.247a1.125 1.125 0 0 1 1.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.086.22-.128.332-.183.582-.495.644-.869l.214-1.28Z"
      />
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
      />
    </svg>

    <svg
      v-if="name == 'computer'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="2.0"
      stroke="currentColor"
      class="size-8"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M9 17.25v1.007a3 3 0 0 1-.879 2.122L7.5 21h9l-.621-.621A3 3 0 0 1 15 18.257V17.25m6-12V15a2.25 2.25 0 0 1-2.25 2.25H5.25A2.25 2.25 0 0 1 3 15V5.25m18 0A2.25 2.25 0 0 0 18.75 3H5.25A2.25 2.25 0 0 0 3 5.25m18 0V12a2.25 2.25 0 0 1-2.25 2.25H5.25A2.25 2.25 0 0 1 3 12V5.25"
      />
    </svg>

    <svg
      v-if="name == 'check3'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="2.0"
      stroke="currentColor"
      class="size-8"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
      />
    </svg>

    <svg
      v-if="name == 'exclamationmark'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z"
      />
    </svg>

    <svg
      v-if="name == 'eye-open'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-4"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z"
      />
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
      />
    </svg>

    <svg
      v-if="name == 'eye-close'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-4"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88"
      />
    </svg>

    <svg
      v-if="name == 'arrow-down1'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-4"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="m19.5 8.25-7.5 7.5-7.5-7.5"
      />
    </svg>

    <svg
      v-if="name == 'graph'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-4"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M10.5 6a7.5 7.5 0 1 0 7.5 7.5h-7.5V6Z"
      />
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M13.5 10.5H21A7.5 7.5 0 0 0 13.5 3v7.5Z"
      />
    </svg>

    <svg
      v-if="name == 'shield'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-12"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M9 12.75 11.25 15 15 9.75m-3-7.036A11.959 11.959 0 0 1 3.598 6 11.99 11.99 0 0 0 3 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285Z"
      />
    </svg>

    <svg
      v-if="name == '3dots'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-6"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M6.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM12.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM18.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z"
      />
    </svg>

    <svg
      v-if="name == 'calendar'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5m-9-6h.008v.008H12v-.008ZM12 15h.008v.008H12V15Zm0 2.25h.008v.008H12v-.008ZM9.75 15h.008v.008H9.75V15Zm0 2.25h.008v.008H9.75v-.008ZM7.5 15h.008v.008H7.5V15Zm0 2.25h.008v.008H7.5v-.008Zm6.75-4.5h.008v.008h-.008v-.008Zm0 2.25h.008v.008h-.008V15Zm0 2.25h.008v.008h-.008v-.008Zm2.25-4.5h.008v.008H16.5v-.008Zm0 2.25h.008v.008H16.5V15Z"
      />
    </svg>

    <svg
      v-if="name == 'calendar1'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-4"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5m-9-6h.008v.008H12v-.008ZM12 15h.008v.008H12V15Zm0 2.25h.008v.008H12v-.008ZM9.75 15h.008v.008H9.75V15Zm0 2.25h.008v.008H9.75v-.008ZM7.5 15h.008v.008H7.5V15Zm0 2.25h.008v.008H7.5v-.008Zm6.75-4.5h.008v.008h-.008v-.008Zm0 2.25h.008v.008h-.008V15Zm0 2.25h.008v.008h-.008v-.008Zm2.25-4.5h.008v.008H16.5v-.008Zm0 2.25h.008v.008H16.5V15Z"
      />
    </svg>

    <svg
      v-if="name == 'add-account1.1'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-4"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M12 4.5v15m7.5-7.5h-15"
      />
    </svg>

    <svg
      v-if="name == 'arrow-left'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-4"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M15.75 19.5 8.25 12l7.5-7.5"
      />
    </svg>

    <svg
      v-if="name == 'arrow-right'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-4"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="m8.25 4.5 7.5 7.5-7.5 7.5"
      />
    </svg>

    <svg
      v-if="name == 'check1'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
      />
    </svg>

    <svg
      v-if="name == 'noticeBell'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5m-9-6h.008v.008H12v-.008ZM12 15h.008v.008H12V15Zm0 2.25h.008v.008H12v-.008ZM9.75 15h.008v.008H9.75V15Zm0 2.25h.008v.008H9.75v-.008ZM7.5 15h.008v.008H7.5V15Zm0 2.25h.008v.008H7.5v-.008Zm6.75-4.5h.008v.008h-.008v-.008Zm0 2.25h.008v.008h-.008V15Zm0 2.25h.008v.008h-.008v-.008Zm2.25-4.5h.008v.008H16.5v-.008Zm0 2.25h.008v.008H16.5V15Z"
      />
    </svg>

    <svg
      v-if="name == 'folder'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-4"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M2.25 12.75V12A2.25 2.25 0 0 1 4.5 9.75h15A2.25 2.25 0 0 1 21.75 12v.75m-8.69-6.44-2.12-2.12a1.5 1.5 0 0 0-1.061-.44H4.5A2.25 2.25 0 0 0 2.25 6v12a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9a2.25 2.25 0 0 0-2.25-2.25h-5.379a1.5 1.5 0 0 1-1.06-.44Z"
      />
    </svg>

    <svg
      v-if="name == 'arrow-path'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="2.0"
      stroke="currentColor"
      class="size-4"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99"
      />
    </svg>
  </div>
</template>
<script>
export default {
  props: ["name"],
  name: "iconPage",
};
</script>
<style scoped></style>
