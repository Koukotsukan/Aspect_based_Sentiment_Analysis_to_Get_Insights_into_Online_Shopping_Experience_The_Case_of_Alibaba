document.addEventListener("DOMContentLoaded", function() {
    const currentPath = window.location.pathname;
    const menuItems = document.querySelectorAll('.nav li a');
    const menuToggle = document.getElementById("menu-toggle");
    const nav = document.querySelector(".nav");


    // Highlight current page in menu
    menuItems.forEach(menuItem => {
        const menuItemLink = menuItem.getAttribute('href');
        if (currentPath === menuItemLink) {
            menuItem.style.color = "#000000";
            menuItem.style.borderBottom = "2px solid #af2639";
        } else {
            menuItem.style.color = "rgba(0, 0, 0, 0.4)";
        }
    });

    // Menu toggle functionality
    menuToggle.addEventListener("click", function () {
        nav.classList.toggle("show");
    });

    var originalContent = null; // 用于存储原始内容
    var isMerged = false; // 标记内容是否已合并

    function adjustLayout() {
        const screenWidth = window.innerWidth;
        const leftDivs = document.querySelectorAll('.left');

        // 当屏幕宽度小于 768px 且内容尚未合并时
        if (screenWidth < 768 && !isMerged) {
            if (leftDivs.length >= 2) {
                originalContent = []; // 初始化数组以存储原始内容
                leftDivs.forEach(div => {
                    originalContent.push(div.innerHTML); // 存储每个 div 的内容
                });

                // 合并第二个 div 的内容到第一个 div，并移除第二个 div
                leftDivs[0].innerHTML += leftDivs[1].innerHTML;
                leftDivs[1].parentNode.removeChild(leftDivs[1]);

                isMerged = true; // 标记已合并
            }
        } else if (screenWidth >= 768 && isMerged) {
            // 当屏幕宽度大于或等于 768px 且内容已合并时，恢复原始布局
            const container = leftDivs[0].parentNode; // 获取父容器
            container.innerHTML = ''; // 清空当前内容

            originalContent.forEach(content => {
                const newDiv = document.createElement('div');
                newDiv.classList.add('left');
                newDiv.innerHTML = content;
                container.appendChild(newDiv); // 重新添加 div 元素
            });

            isMerged = false; // 标记已恢复
        }
    }

    adjustLayout(); // 页面加载时执行
    window.addEventListener('resize', adjustLayout); // 窗口大小改变时执行
	function initializeImageModal() {
    var modal = document.getElementById("myModal");
    var modalImg = document.getElementById("img01");
    var captionText = document.getElementById("caption");
    var span = document.getElementsByClassName("close")[0];

    function openModal(image) {
        modal.style.display = "block";
        modalImg.src = image.src;
        captionText.innerHTML = image.alt;
    }

    var images = document.getElementsByClassName("myImg");
    for (var i = 0; i < images.length; i++) {
        var img = images[i];

        // 对于桌面端，使用 click 事件
        img.addEventListener('click', function() {
            openModal(this);
        });

        // 对于移动端，使用 touchend 事件
        let touchMoved;
        img.addEventListener('touchstart', function() {
            touchMoved = false;
        });
        img.addEventListener('touchmove', function() {
            touchMoved = true;
        });
        img.addEventListener('touchend', function() {
            if (!touchMoved) {
                openModal(this);
            }
        });
    }

    span.addEventListener('click', function() { 
        modal.style.display = "none";
    });
}
    initializeImageModal();
});
