.PHONY: init build migrate up

init:
	@mkdir -p ${PWD}/${BASE_LOG_DIR}
	@mkdir -p ${PWD}/${BASE_LOG_DIR_SHOW_SERVICE}
	@mkdir -p ${PWD}/${BASE_LOG_DIR_PAYMENT_SERVICE}
	@mkdir -p ${PWD}/${BASE_LOG_DIR_STORAGE_SERVICE}

deploy: init
	@docker compose up --build
