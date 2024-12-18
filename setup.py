from cx_Freeze import setup, Executable

# 의존성 패키지 목록
build_exe_options = {
    "packages": ["tkinter", "socket", "csv", "datetime", "threading"],
    "include_files": [],  # 추가 파일이 필요한 경우 여기에 추가
    "excludes": []
}

setup(
    name="은성_데이터 수신 프로그램",
    version="1.0",
    description="UDP 데이터 수신 및 CSV 저장 프로그램",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "demo.py",
            base="Win32GUI",  # Windows GUI 애플리케이션으로 설정
            target_name="은성_데이터수신프로그램.exe",  # 생성될 실행 파일 이름
            icon=None  # 아이콘 파일이 필요한 경우 경로 지정
        )
    ]
)
