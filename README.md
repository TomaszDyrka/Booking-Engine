# BookingEngine - System Rezerwacji Sal Konferencyjnych

## Przegląd
Kompleksowy system rezerwacji sal konferencyjnych zaprojektowany z wykorzystaniem modułowej architektury backendowej, aby zoptymalizować przepływ danych i zapobiegać konfliktom w harmonogramie. Projekt skupia się na solidnej infrastrukturze, systematycznych testach oraz niezawodnej izolacji środowisk.

## Stos Technologiczny
* **Backend:** Python, Django
* **Baza danych:** PostgreSQL
* **Konteneryzacja:** Docker, Docker Compose
* **CI/CD i Testy:** GitLab CI

## Infrastruktura i Automatyzacja
* **Architektura wielokontenerowa:** Wykorzystuje Docker Compose do ścisłej izolacji usługi backendowej Django od instancji bazy danych PostgreSQL, używając dedykowanych sieci kontenerów i zautomatyzowanego zarządzania wolumenami.
* **Zoptymalizowane budowanie:** Wdraża wieloetapowe budowanie obrazów (multi-stage Docker builds), aby zagwarantować absolutną spójność środowiska w fazach rozwoju lokalnego i testowania, przy jednoczesnej optymalizacji rozmiaru obrazów.
* **Integracja CI/CD:** Skonteneryzowane środowiska są płynnie zintegrowane ze zautomatyzowanymi przepływami testowymi w ramach potoków GitLab CI/CD. Zapewnia to szybką pętlę zwrotną i eliminuje błędy związane ze środowiskiem na wczesnym etapie dostarczania.

## Konfiguracja Lokalna

1. **Sklonuj repozytorium:**
```
git clone <repository-url>
cd booking-app
```

2. **Zbuduj i uruchom kontenery:**
```
docker compose -f docker-compose.yml --profile prod up
```

3. **Korzystaj!**

Domyślne konto admina ma dane:
- email: admin@test.com
- hasło: 1234

Aplikacja jest dostępna na adresach:** 
- dla użytkowników: 0.0.0.0/ 
- dla adminów:      0.0.0.0/admin

## Testowanie
Wszystkie testy są uruchamiane automatycznie w GitLab CI, ale możesz je również odpalić lokalnie w swoim izolowanym kontenerze:
```
docker exec bookingengine-backend-prod-1 uv run python -m pytest
```

## Autor
**Tomasz Dyrka**