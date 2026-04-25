/* Tag autocomplete functionality */
(function() {
    'use strict';

    // 初始化标签自动补全
    function initTagAutocomplete() {
        var tagInput = document.getElementById('tags');
        if (!tagInput) return;

        var autocompleteList = document.createElement('div');
        autocompleteList.className = 'tag-autocomplete-list';
        tagInput.parentNode.style.position = 'relative';
        tagInput.parentNode.appendChild(autocompleteList);

        var allTags = [];
        var currentFocus = -1;

        // 从 API 获取所有标签
        fetch('/api/tags')
            .then(response => response.json())
            .then(data => {
                allTags = data.tags || [];
            })
            .catch(error => console.error('Error fetching tags:', error));

        // 输入事件处理
        tagInput.addEventListener('input', function(e) {
            var val = this.value;
            closeAllLists();
            currentFocus = -1;

            if (!val) return;

            // 获取当前正在输入的标签（最后一个逗号后的内容）
            var lastCommaIndex = val.lastIndexOf(',');
            var currentTag = lastCommaIndex >= 0 ? val.substring(lastCommaIndex + 1).trim() : val.trim();

            if (!currentTag) return;

            // 过滤匹配的标签
            var matches = allTags.filter(function(tag) {
                return tag.toLowerCase().indexOf(currentTag.toLowerCase()) !== -1;
            });

            if (matches.length === 0) return;

            // 显示匹配的标签
            matches.forEach(function(tag) {
                var item = document.createElement('div');
                item.className = 'tag-autocomplete-item';

                // 高亮匹配部分
                var matchIndex = tag.toLowerCase().indexOf(currentTag.toLowerCase());
                var beforeMatch = tag.substr(0, matchIndex);
                var match = tag.substr(matchIndex, currentTag.length);
                var afterMatch = tag.substr(matchIndex + currentTag.length);

                item.innerHTML = beforeMatch + '<strong>' + match + '</strong>' + afterMatch;
                item.innerHTML += '<input type="hidden" value="' + tag + '">';

                // 点击选择标签
                item.addEventListener('click', function(e) {
                    var selectedTag = this.getElementsByTagName('input')[0].value;

                    // 替换当前正在输入的标签
                    if (lastCommaIndex >= 0) {
                        tagInput.value = val.substring(0, lastCommaIndex + 1) + ' ' + selectedTag + ', ';
                    } else {
                        tagInput.value = selectedTag + ', ';
                    }

                    closeAllLists();
                    tagInput.focus();
                });

                autocompleteList.appendChild(item);
            });
        });

        // 键盘导航
        tagInput.addEventListener('keydown', function(e) {
            var items = autocompleteList.getElementsByClassName('tag-autocomplete-item');

            if (e.keyCode === 40) { // Down arrow
                e.preventDefault();
                currentFocus++;
                addActive(items);
            } else if (e.keyCode === 38) { // Up arrow
                e.preventDefault();
                currentFocus--;
                addActive(items);
            } else if (e.keyCode === 13) { // Enter
                if (currentFocus > -1 && items[currentFocus]) {
                    e.preventDefault();
                    items[currentFocus].click();
                }
            } else if (e.keyCode === 27) { // Escape
                closeAllLists();
            }
        });

        function addActive(items) {
            if (!items || items.length === 0) return;
            removeActive(items);

            if (currentFocus >= items.length) currentFocus = 0;
            if (currentFocus < 0) currentFocus = items.length - 1;

            items[currentFocus].classList.add('tag-autocomplete-active');
        }

        function removeActive(items) {
            for (var i = 0; i < items.length; i++) {
                items[i].classList.remove('tag-autocomplete-active');
            }
        }

        function closeAllLists() {
            autocompleteList.innerHTML = '';
            currentFocus = -1;
        }

        // 点击页面其他地方关闭列表
        document.addEventListener('click', function(e) {
            if (e.target !== tagInput) {
                closeAllLists();
            }
        });
    }

    // DOM 加载完成后初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTagAutocomplete);
    } else {
        initTagAutocomplete();
    }
})();
