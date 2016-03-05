
: ${GOOGLE_APPLICATION_CREDENTIALS:=dummy_secret.json}
: ${GC_VISION_TEST_IMAGE_DIR:=`rospack find gc_vision_bridge`/imgs}

export GOOGLE_APPLICATION_CREDENTIALS 
export GC_VISION_TEST_IMAGE_DIR
