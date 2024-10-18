import sys
from dotenv import load_dotenv, set_key, dotenv_values

# .env 파일 경로
env_path = ".env"

# .env 파일 로드
load_dotenv(env_path)

# 함수: 특정 키의 값을 변경
def update_env_value(key, new_value):
    set_key(env_path, key, new_value)
    print(f"{key} 값을 {new_value}로 업데이트 했습니다.")

# 명령줄 인자로 값을 받음
if len(sys.argv) != 4:
    print(f" .env 파일 내 값을 업데이트 합니다 / UDID - {sys.argv[1]}, PLATFORM_VERSION - {sys.argv[2]}")
    sys.exit(1)

udid_input = sys.argv[1]
version_input = sys.argv[2]
os_type_input = sys.argv[3]

if os_type_input == "ios":
    update_env_value("IOS_UDID", udid_input)
    update_env_value("IOS_PLATFORM_VERSION", version_input)
elif os_type_input == "android":
    update_env_value("ANDROID_UDID", udid_input)
    update_env_value("ANDROID_PLATFORM_VERSION", version_input)
else:
    print("유효하지 않은 OS 유형입니다.")
    sys.exit(1)