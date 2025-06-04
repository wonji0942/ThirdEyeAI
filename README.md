# ThirdEyeAI

# 깃허브 협업 관련 주의 사항(06.04 수정)

# 데이터 전처리 과정 및 데이터 업로드 방식
로보플로에서 라벨링 작업 수행
roboflow API를 이용해 코랩에서 데이터셋 업로드해서 YOLOv8 모델 학습시킴.

# 학습된 모델(best.pt) 저장 위치
https://drive.google.com/drive/u/0/folders/1GNMjEyf6C05ZU5AT6XG_YVqMGQVfBGed
-> 모델 이용 시, 구글드라이브에서 최종 best.pt 다운로드해서 로컬에서 이용하면 됨됨.

# 모델 학습 후 변경사항 깃허브 업로드 방식
-학습 완료 후 best.pt 파일은 위 드라이브에 업로드해두기(폴더명 명시시)
-코랩에서 돌린 .ipynb 파일에서 상단 탭 (수정>모든 출력 지우기)를 하고 파일 저장
-로컬의 ThirdEyeAI 폴더 내에 .ipynb 파일 위치시키고, 깃허브에 업로드
-개인 브랜치(예:dev_yhy)에 push -> 깃헙 사이트에 와서 개인브랜치->colab 브랜치로 PR 날리고 담당자에게 merge 요청하기
(commit 메시지에 학습 결과 그래프 캡쳐해서 넣기)
