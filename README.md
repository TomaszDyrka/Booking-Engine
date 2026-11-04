# BookingEngine - System Rezerwacji Sal Konferencyjnych

## Przegląd
System rezerwacji sal konferencyjnych zaprojektowany z wykorzystaniem modułowej architektury backendowej oraz .

## Stos Technologiczny
* **Backend:** Python, Django
* **Baza danych:** PostgreSQL
* **Konteneryzacja:** Docker
* **Orkiestracja:** Kubernetes, Docker Compose, Minikube
* **CI/CD i Testy:** GitLab CI, pytest

## Infrastruktura i Automatyzacja
* **Konteneryzacja (Docker Compose)**: Backend (Django) i baza danych (PostgreSQL) działają w odizolowanych kontenerach, ze skonfigurowaną siecią i wolumenem dla zachowania danych.
* **Multi-stage builds**: Proces budowania obrazów Docker jest wieloetapowy, co minimalizuje ich rozmiar docelowy i zapewnia to samo środowisko do testów oraz developmentu.
* **GitLab CI/CD**: Pipeline'y automatycznie uruchamiają testy w kontenerach przy każdej zmianie w kodzie.
* **Manifesty Kubernetes**: Aplikacja jest przygotowana do wdrożenia w chmurze lub lokalnie na Minikube za pomocą napisanych konfiguracji K8s.

## Konfiguracja Lokalna

1. **Sklonuj repozytorium:**
```
git clone <repository-url>
cd booking-app
```

2. **Zmień nazwę folderu .env_example na .env_dir**

3. **Uzupełnij zmienne środowiskowe**

4. **Zbuduj i uruchom kontenery:**
```
docker compose -f docker-compose.yml --profile prod up
```

5. **Korzystaj!**

Aplikacja pojawia się na localhoście.
Domyślne konto admina ma dane:
- email: admin@test.com
- hasło: podane w zmiennych środowiskowych
Co może być zmienione m.in. poprzez modyfikację pliku compose.

6. **\*Uruchom na minikube**

Aby uruchomić aplikację na minikube, należy:
- zbudować i załadować oba obrazy do minikube:
    - `docker build -t django-app:prod -f Dockerfile.Backend .`
    - `docker build -t nginx-frontend -f Dockerfile.Frontend .`
    - `minikube image load <obraz>`
- zalecić utworzenie zasobów: `kubectl apply -k .`
- udostępnić serwis nginx'a komputerowi poleceniem: `minikube tunnel` (należy to zrobić ponieważ chcemy 'zasymulować' load balancer)
- poleceniem `kubectl get svc -n booking-namespace` sprawdzić external IP tego service (adres do użycia w przeglądarce)
- ewentualnie jeśli minikube działa na maszynie wirtualnej wewnątrz komputera - ustawić połączenie rzutujące porty (np. `ssh -L <port-hosta>:<external ip>:80 user@vm-ip`)

## Testowanie
Wszystkie testy są uruchamiane automatycznie w GitLab CI, ale możesz je również odpalić lokalnie w profilu *backend-test* w docker-compose, np:
```
docker compose --profile backend-test up backend-test --build
```

## Autor
**Tomasz Dyrka**
