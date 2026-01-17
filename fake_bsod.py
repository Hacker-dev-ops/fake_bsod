import pygame
import time
import sys
import keyboard
import math

# ================== БЛОКИРОВКА КЛАВИАТУРЫ ==================

blocked = False

def block_keyboard():
    global blocked
    if blocked:
        return
    keyboard.on_press(lambda e: None, suppress=True)
    blocked = True

def unblock_keyboard():
    global blocked
    keyboard.unhook_all()
    blocked = False

# ================== ЗВУК ОШИБКИ WINDOWS ==================

def play_error_sound():
    sample_rate = 44100
    duration = 0.6
    freq = 440

    n_samples = int(sample_rate * duration)
    buf = bytearray()

    for i in range(n_samples):
        v = int(32767 * math.sin(2 * math.pi * freq * i / sample_rate))
        buf += v.to_bytes(2, byteorder="little", signed=True)

    sound = pygame.mixer.Sound(buffer=buf)
    sound.play()

# ================== PYGAME + МОНИТОРЫ ==================

pygame.init()
pygame.mixer.init()

num_displays = pygame.display.get_num_displays()
screens = []

for i in range(num_displays):
    screen = pygame.display.set_mode(
        (pygame.display.Info().current_w, pygame.display.Info().current_h),
        pygame.NOFRAME,
        display=i
    )
    screens.append(screen)

pygame.mouse.set_visible(False)

BLUE = (0, 120, 215)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

font_big = pygame.font.SysFont("Segoe UI", 120)
font_mid = pygame.font.SysFont("Segoe UI", 36)
font_small = pygame.font.SysFont("Segoe UI", 24)
font_bios = pygame.font.SysFont("Consolas", 22)

# ================== ОТРИСОВКА НА ВСЕ МОНИТОРЫ ==================

def draw_all(draw_func):
    for screen in screens:
        draw_func(screen)
    pygame.display.flip()

# ================== ФЕЙКОВЫЙ BSOD ==================

def fake_bsod(code):
    play_error_sound()
    percent = 0
    while percent <= 100:
        def draw(screen):
            screen.fill(BLUE)
            screen.blit(font_big.render(":(", True, WHITE), (100, 80))
            screen.blit(font_mid.render(
                "На вашем компьютере возникла проблема, и его необходимо перезагрузить.", True, WHITE
            ), (100, 250))
            screen.blit(font_mid.render(
                "Мы лишь собираем некоторые сведения об ошибке, а затем будет выполнена перезагрузка.", True, WHITE
            ), (100, 300))
            screen.blit(font_mid.render(f"{percent}% выполнено", True, WHITE), (100, 360))
            screen.blit(font_small.render(
                "Если вы хотите узнать больше, выполните поиск в Интернете по следующему коду ошибки:", True, WHITE
            ), (100, 440))
            screen.blit(font_small.render(code, True, WHITE), (100, 470))

        draw_all(draw)
        percent += 1
        time.sleep(0.06)
        for event in pygame.event.get():
            pass

# ================== ФЕЙКОВЫЙ REBOOT ==================

def fake_reboot(sec=3):
    start = time.time()
    while time.time() - start < sec:
        def draw(screen):
            screen.fill(BLACK)
            dots = int((time.time() - start) % 4)
            txt = font_mid.render("Выполняется перезагрузка" + "." * dots, True, WHITE)
            screen.blit(txt, (200, 400))
        draw_all(draw)
        time.sleep(0.5)

# ================== ФЕЙКОВЫЙ BIOS ==================

def fake_bios(sec=5):
    start = time.time()
    while time.time() - start < sec:
        def draw(screen):
            screen.fill(BLACK)
            lines = [
                "American Megatrends Inc.",
                "BIOS Version 2.17.1246",
                "",
                "CPU: Intel(R) Core(TM) i7",
                "Memory Test: 16384MB OK",
                "",
                "Detecting IDE Drives...",
                "SATA Port 1: SSD OK",
                "USB Devices: 2 Found",
                "",
                "Press DEL to enter Setup",
            ]
            y = 80
            for line in lines:
                screen.blit(font_bios.render(line, True, GREEN), (60, y))
                y += 30

        draw_all(draw)
        time.sleep(0.1)

# ================== СЦЕНАРИЙ ==================

block_keyboard()

fake_bsod("CRITICAL_PROCESS_DIED")
fake_reboot(3)
fake_bios(5)
fake_bsod("KERNEL_SECURITY_CHECK_FAILURE")
fake_reboot(3)
fake_bsod("CRITICAL_PROCESS_DIED")
fake_bios(5)
fake_bsod("CRITICAL_PROCESS_DIED")
fake_reboot(3)
fake_bsod("PAGE_FAULT_IN_NONPAGED_AREA")
fake_reboot(6)
fake_bsod("MEMORY_MANAGEMENT")
fake_bsod("ERROR_REBOOT_REQUIRED")
fake_bsod("SYSTEM_SERVICE_EXCEPTION")
fake_reboot(4)
fake_bsod("CRITICAL_PROCESS_DIED")
fake_bsod("KERNEL_SECURITY_CHECK_FAILURE")
fake_reboot(5)
fake_bsod("ERROR_REBOOT")
fake_reboot(27)

unblock_keyboard()

pygame.quit()
sys.exit()
