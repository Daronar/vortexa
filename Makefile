build:
	docker build -t mp_test_assignment_image .

run:
	mkdir -p result_from_docker
	docker run -it --rm --name=mp_test_assignment \
	-e PATH_TO_RESULT_FILE=/results/storage_asof_20200114.csv \
	-e USE_MULTIPROCESSING=True \
	-e MAX_DATETIME='14/01/2020 00:00:00' \
	-v $(PWD)/result_from_docker:/results mp_test_assignment_image

test:
	pytest ./tests