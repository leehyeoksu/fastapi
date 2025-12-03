document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('messageForm');
    const errorMessage = document.getElementById('errorMessage');
    const submitBtn = form.querySelector('.submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoading = submitBtn.querySelector('.btn-loading');

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        // 폼 데이터 수집
        const formData = {
            name: document.getElementById('name').value.trim(),
            value: document.getElementById('value').value.trim(),
            description: document.getElementById('description').value.trim() || null
        };

        // 유효성 검사
        if (!formData.name || !formData.value) {
            showError('이름과 메시지는 필수 입력 항목입니다.');
            return;
        }

        // 로딩 상태
        submitBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoading.style.display = 'inline';
        errorMessage.classList.remove('show');

        try {
            // API 호출
            const response = await fetch('/data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || '서버 오류가 발생했습니다.');
            }

            const data = await response.json();

            // 성공 페이지로 리디렉션 (데이터를 URL 파라미터로 전달)
            const dataParam = encodeURIComponent(JSON.stringify(data));
            window.location.href = `/success?data=${dataParam}`;

        } catch (error) {
            console.error('Error:', error);
            showError(error.message || '메시지 전송에 실패했습니다.');

            // 로딩 상태 해제
            submitBtn.disabled = false;
            btnText.style.display = 'inline';
            btnLoading.style.display = 'none';
        }
    });

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.classList.add('show');

        // 3초 후 자동으로 에러 메시지 숨김
        setTimeout(() => {
            errorMessage.classList.remove('show');
        }, 3000);
    }
});
