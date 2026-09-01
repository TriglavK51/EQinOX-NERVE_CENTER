# PLAN_PRACY

## Kolejnosc pracy agenta

1. Przeczytaj caly ten plik przed rozpoczeciem edycji lub uruchamiania kodu.
2. Uruchom Nerve Center z katalogu, do ktorego zostal sklonowany:
   ```powershell
   & "<SCIEZKA_DO_NERVE_CENTER>\setup.ps1" -Start
   ```
3. Potwierdz, ze `http://127.0.0.1:8088/healthz` zwraca status `ok`.
4. Przeczytaj `<SCIEZKA_DO_NERVE_CENTER>\SKILL.md` oraz manifesty z
   `http://127.0.0.1:8088/.well-known/tools`.
5. Dobierz lokalne skille zgodnie z Nerve Center, a nastepnie realizuj ponizsze wytyczne projektu.

## Wytyczne projektu

Zastap ta sekcje wymaganiami, architektura i kolejnoscia implementacji dla tego workspace.