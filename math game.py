import pygame
import random
import time
import math

# เริ่มต้น pygame
pygame.init()

# กำหนดขนาดหน้าจอ
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Math Quiz Battle")

# กำหนดสี
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

# กำหนดฟอนต์
font = pygame.font.SysFont(None, 40)

# โหลดภาพพื้นหลัง
background_image = pygame.image.load('background.jpg')  # ใส่ชื่อไฟล์ของภาพพื้นหลังที่นี่
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# โหลดเสียง
pygame.mixer.init()
start_music = 'bgstart.mp3'
game_music = 'bgmusic.mp3'
winner_music = 'win.mp3'
warning_sound = 'warn.wav'
correct_sound = pygame.mixer.Sound('correct.wav')
incorrect_sound = pygame.mixer.Sound('wrong.wav')

# ฟังก์ชันสำหรับวาดปุ่มพร้อมภาพพื้นหลัง
def draw_button_with_bg(screen, rect, bg_image, text, font, text_color=white):
    button_bg = pygame.image.load(bg_image)
    button_bg = pygame.transform.scale(button_bg, rect.size)
    screen.blit(button_bg, rect.topleft)

    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def message_to_screen(msg, color, rect):
    text = font.render(msg, True, color)
    text_rect = text.get_rect(center=rect.center)
    screen.blit(text, text_rect)

def generate_question():
    operations = ['+', '-', '*', '/', 'sqrt', 'log']
    operation = random.choice(operations)

    if operation in ['+', '-']:
        num1 = round(random.uniform(1, 20), 2)
        num2 = round(random.uniform(1, 20), 2)
        question = f"{num1} {operation} {num2}"
        answer = round(eval(question), 2)
    elif operation == '*':
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        question = f"{num1} {operation} {num2}"
        answer = num1 * num2
    elif operation == '/':
        num2 = random.randint(1, 20)
        answer = random.randint(1, 20)
        num1 = num2 * answer
        question = f"{num1} {operation} {num2}"
    elif operation == 'sqrt':
        num = random.choice([1, 4, 9, 16, 25, 36, 49, 64, 81, 100])
        question = f"sqrt({num})"
        answer = int(math.sqrt(num))
    elif operation == 'log':
        base = random.randint(2, 5)
        num = base ** random.randint(1, 3)
        question = f"log{base}({num})"
        answer = int(math.log(num, base))

    # สร้างช้อยส์
    choices = [answer]

    # เพิ่มช้อยส์ที่ไม่ใช่คำตอบ
    while len(choices) < 3:
        if operation in ['+', '-']:
            choice = round(answer + random.uniform(-10, 10), 2)
        else:
            choice = answer + random.randint(-10, 10)

        if choice not in choices and (operation in ['+', '-'] or isinstance(choice, int)):
            choices.append(choice)

    # สุ่มลำดับช้อยส์
    random.shuffle(choices)

    return question, answer, choices

def display_start_menu():
    screen.blit(background_image, (0, 0))
    pygame.mixer.music.load(start_music)
    pygame.mixer.music.play(-1)
    
    title_bg = 'title.png'
    draw_button_with_bg(screen, pygame.Rect(screen_width / 2 - 300, screen_height / 2 - 400, 600, 500), title_bg, "", font)
 
    # โหลดและวาดรูปภาพตรงกลางระหว่าง Title และปุ่ม Start
    center_image = pygame.image.load('vs.png')  # ใส่ชื่อไฟล์รูปภาพที่ต้องการ
    center_image = pygame.transform.scale(center_image, (150, 150))  # ปรับขนาดรูปภาพตามต้องการ
    center_image_rect = center_image.get_rect(center=(screen_width / 2, screen_height / 2 - 50))
    screen.blit(center_image, center_image_rect)

    start_button_rect = pygame.Rect(screen_width / 2 - 150, screen_height / 2, 300, 75)
    start_button_bg = 'button.png'
    draw_button_with_bg(screen, start_button_rect, start_button_bg, "Start Game", font, text_color=black)

    exit_button_rect = pygame.Rect(screen_width / 2 - 150, screen_height / 2 + 100, 300, 75)
    exit_button_bg = 'button.png'
    draw_button_with_bg(screen, exit_button_rect, exit_button_bg, "Exit", font, text_color=black)

    pygame.display.update()

    return start_button_rect, exit_button_rect

def load_high_scores():
    try:
        with open('high_scores.txt', 'r', encoding='utf-8') as file:
            scores = file.readlines()
            high_scores = [line.strip().split(',') for line in scores]
            return high_scores
    except FileNotFoundError:
        return []

def save_high_scores(player_name, score):
    high_scores = load_high_scores()
    
    # Check if the player's name is already in the high scores
    player_exists = False
    for i, (name, old_score) in enumerate(high_scores):
        if name == player_name:
            # Update score if new score is higher
            if int(score) > int(old_score):
                high_scores[i] = [player_name, str(score)]
            player_exists = True
            break
    
    # If player doesn't exist in high scores, add them
    if not player_exists:
        high_scores.append([player_name, str(score)])
    
    # Sort high scores and keep only the top 5
    high_scores.sort(key=lambda x: int(x[1]), reverse=True)
    high_scores = high_scores[:5]
    
    # Save to file
    with open('high_scores.txt', 'w', encoding='utf-8') as file:
        for name, score in high_scores:
            file.write(f"{name},{score}\n")

def display_high_scores():
    high_scores = load_high_scores()  # โหลดคะแนนสูง
    y_offset = 200  # กำหนดตำแหน่งแนวตั้งเริ่มต้น
    
    # วาดภาพพื้นหลังหลักของหน้าจอ
    screen.blit(background_image, (0, 0))  # วาดภาพพื้นหลังหลักที่ตำแหน่ง (0, 0) ของหน้าจอ

    # โหลดและวาดพื้นหลังสำหรับข้อความ "High Scores:"
    score_background_image = pygame.image.load('high score.jpg')  # โหลดภาพ PNG สำหรับพื้นหลังข้อความ
    score_background_image = pygame.transform.scale(score_background_image, (300, 60))  # ปรับขนาดตามต้องการ
    screen.blit(score_background_image, (screen_width / 2 - 150, y_offset - 20))  # วาดพื้นหลังที่ตำแหน่งที่ต้องการ

    # แสดงข้อความ "High Scores:"
    message_to_screen("High Scores:", black, pygame.Rect(screen_width / 2 - 100, y_offset, 200, 50))
    y_offset += 50  # เลื่อนตำแหน่งแนวตั้งสำหรับการแสดงคะแนน

    # แสดงคะแนนสูง
    for i, (name, score) in enumerate(high_scores[:5]):  # แสดงเฉพาะ 5 อันดับแรก
        message_to_screen(f"{i + 1}. {name} - {score}", black, pygame.Rect(screen_width / 2 - 100, y_offset, 200, 50))
        y_offset += 50  # เลื่อนตำแหน่งแนวตั้งสำหรับคะแนนถัดไป

    pygame.display.update()  # อัพเดทหน้าจอเพื่อแสดงผล

    # รอ 3 วินาทีแล้วกลับไปที่เมนูหลัก
    time.sleep(3)
    main()  # เรียกใช้งานฟังก์ชันหลักเพื่อกลับไปที่เมนูหลัก

def get_player_names(player_number):
    input_box = pygame.Rect(screen_width / 2 - 150, screen_height / 2 - 50, 300, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('darkorange3')
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.Font(None, 74)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        txt_surface = font.render(text, True, color)
        width = max(300, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)

        # แสดงข้อความอธิบาย
        prompt_surface = font.render(f"Enter Player {player_number}'s Name:", True, white)
        prompt_rect = prompt_surface.get_rect(center=(screen_width / 2, screen_height / 2 - 100))
        screen.blit(prompt_surface, prompt_rect)

        pygame.display.flip()
        clock.tick(30)

def game_loop():
    pygame.mixer.music.load(game_music)
    pygame.mixer.music.play(-1)

    game_exit = False
    player1_score = 0
    player2_score = 0
    total_time = 60
    start_time = time.time()
    penalty = 1
    warning_played = False
    blink = False

    player1_name = get_player_names(1)
    player2_name = get_player_names(2)

    question, correct_answer, choices = generate_question()

    choice_rects = [
        pygame.Rect(100, 400, 250, 100),
        pygame.Rect(500, 400, 250, 100),
        pygame.Rect(900, 400, 250, 100)
    ]
    
    answered = False

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

            keys = pygame.key.get_pressed()
            if not answered:
                if keys[pygame.K_1]:
                    if choices[0] == correct_answer:
                        player1_score += 1
                        correct_sound.play()
                    else:
                        player1_score = max(0, player1_score - penalty)
                        incorrect_sound.play()
                    answered = True
                elif keys[pygame.K_2]:
                    if choices[1] == correct_answer:
                        player1_score += 1
                        correct_sound.play()
                    else:
                        player1_score = max(0, player1_score - penalty)
                        incorrect_sound.play()
                    answered = True
                elif keys[pygame.K_3]:
                    if choices[2] == correct_answer:
                        player1_score += 1
                        correct_sound.play()
                    else:
                        player1_score = max(0, player1_score - penalty)
                        incorrect_sound.play()
                    answered = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not answered:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, rect in enumerate(choice_rects):
                        if rect.collidepoint(mouse_pos):
                            if choices[i] == correct_answer:
                                player2_score += 1
                                correct_sound.play()
                            else:
                                player2_score = max(0, player2_score - penalty)
                                incorrect_sound.play()
                            answered = True

        if answered:
            question, correct_answer, choices = generate_question()
            choice_rects = [
                pygame.Rect(100, 400, 250, 100),
                pygame.Rect(500, 400, 250, 100),
                pygame.Rect(900, 400, 250, 100)
            ]
            answered = False

        screen.blit(background_image, (0, 0))

        time_left = total_time - (time.time() - start_time)

        if time_left <= 10:
            if not warning_played:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(warning_sound)
                pygame.mixer.music.play(-1)
                warning_played = True
            blink = not blink

        if time_left <= 0:
            game_exit = True

        text_color = red if blink and time_left <= 10 else black
        message_to_screen(f"Time Left: {int(time_left)}", text_color, pygame.Rect(screen_width / 2 - 100, 50, 200, 50))

        message_to_screen(f"Question: {question}", black, pygame.Rect(screen_width / 2 - 200, 100, 400, 50))

        for i, choice in enumerate(choices):
            color = blue if i == 0 else green if i == 1 else red
            pygame.draw.rect(screen, color, choice_rects[i])
            message_to_screen(str(choice), white, choice_rects[i])

        # แสดงคะแนนของผู้เล่นภายในกรอบ
        player1_score_surface = font.render(f"{player1_name}'s Score: {player1_score}", True, red)
        screen.blit(player1_score_surface, (175, 150))
        player2_score_surface = font.render(f"{player2_name}'s Score: {player2_score}", True, blue)
        screen.blit(player2_score_surface, (800, 150))  # ย้ายคะแนนของ player2 ลงมาใต้ player1

        pygame.display.update()

    pygame.mixer.music.stop()
    pygame.mixer.music.load(winner_music)
    pygame.mixer.music.play()

    screen.blit(background_image, (0, 0))
    if player1_score > player2_score:
        message_to_screen(f"{player1_name} Wins!", blue, pygame.Rect(screen_width / 2 - 150, screen_height / 2 - 50, 300, 100))
    elif player2_score > player1_score:
        message_to_screen(f"{player2_name} Wins!", red, pygame.Rect(screen_width / 2 - 150, screen_height / 2 - 50, 300, 100))
    else:
        message_to_screen("It's a Tie!", black, pygame.Rect(screen_width / 2 - 100, screen_height / 2 - 50, 200, 100))

    pygame.display.update()
    time.sleep(3)

    # บันทึกคะแนนก่อน
    save_high_scores(player1_name, player1_score)
    save_high_scores(player2_name, player2_score)

    # แล้วแสดงตารางคะแนน
    display_high_scores()

def main():
    while True:
        start_button, exit_button = display_start_menu()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_button.collidepoint(mouse_pos):
                        game_loop()
                    elif exit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        quit()

if __name__ == "__main__":
    main()