filter:: a filter
title:: A title
- aaa

- SCRUM test

- [#C] Icebox

- [#B] Backlog #T (1 por defecto)

- [#B] Backlog #T/5 (5 horas)

- [#A] Current #T/3

- LATER [#A] Doing #T/1
  :LOGBOOK:
  CLOCK: [2023-07-07 Mon 10:00:00]--[2023-07-07 Mon 11:00:00] =>  01:00:00
  CLOCK: [2023-07-12 Mon 10:00:00]--[2023-07-12 Mon 11:00:00] =>  01:00:00
  :END:

- [#C] Doing #T/23

- DONE Done

- WAITING [#C] Waiting con prioridad ABC #T

- Repetitiva sin prioridad #R
  SCHEDULED: <2024-01-24 Wed>

- [#A] Repetitiva con prioridad #[[R/2]]
  SCHEDULED: <2024-01-26 Fri>

- Todo esto acompañado de un comando que puede buscar grafos en un número indeterminado de rutas o negar ciertas rutas, que puede ser más rápido. Por ejemplo:

- ```shell
  # Buscaría en las rutas siguientes
  mlkgraph /a/b/sunntics /a/b/freelancing

  # Buscaría en la ruta principal pero obviando la ruta -n
  mlkgraph -n /a/b/fun /a/b
  ```
- Sacar reportes por pantalla que se puedan fijar en un TXT con > con facilidad para no tener que ejecutar el parseo constantemente que es duro.
- Todo esto apoyado por **Keep** para esas cosas que no se pueden olvidar sin tener a Logseq cerca, las cosas de casa.
- Aunque también se tiene a la aplicación de GitHub que es capaz de rastrear bien en el repo de Logseq, tanto en tablet como en móvil `user:malkab earthborne rangers` buscará en Logseq y dándole a ver como HTML o Preview veremos el MD renderizado, va realmente bien.

- Current #SCB/1 #SCC/1 #P/Test/a/b
  :LOGBOOK:
  CLOCK: [2023-07-12 Mon 10:00:00]--[2023-07-12 Mon 11:00:00] =>  01:00:00
  CLOCK: [2023-07-17 Mon 10:00:00]--[2023-07-17 Mon 16:00:00] =>  01:00:00
  :END:

- Backlog #SCB/3 #P/Test
  :LOGBOOK:
  CLOCK: [2023-07-07 Mon 10:00:00]--[2023-07-07 Mon 11:00:00] =>  01:00:00
  CLOCK: [2023-07-12 Mon 10:00:00]--[2023-07-12 Mon 11:00:00] =>  01:00:00
  :END:

- DONE Done #P/Test
  :LOGBOOK:
  CLOCK: [2023-07-07 Mon 10:00:00]--[2023-07-07 Mon 11:00:00] =>  01:00:00
  CLOCK: [2023-07-10 Mon 10:00:00]--[2023-07-10 Mon 11:00:00] =>  01:00:00
  :END:

- Another
  :LOGBOOK:
  CLOCK: [2023-07-07 Mon 12:00:00]--[2023-07-07 Mon 13:00:00] =>  01:00:00
  CLOCK: [2023-07-17 Mon 10:00:00]--[2023-07-17 Mon 11:00:00] =>  01:00:00
  :END:

- Current #[[P/A]] #SCB/6 #SCC/3
  :LOGBOOK:
  CLOCK: [2023-07-07 Mon 10:00:00]--[2023-07-07 Mon 11:00:00] =>  01:00:00
  CLOCK: [2023-07-10 Mon 10:00:00]--[2023-07-10 Mon 11:00:00] =>  01:00:00
  :END:

- DONE Done #[[P/Test 2]]
  :LOGBOOK:
  CLOCK: [2024-01-02 Mon 10:00:00]--[2024-01-02 Mon 11:00:00] =>  01:00:00
  CLOCK: [2024-01-29 Mon 10:00:00]--[2024-01-29 Mon 11:00:00] =>  01:00:00
  :END:

- Something without SCRUM #[[P/Test C]]

- Estoy en NOW