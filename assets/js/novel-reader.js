// 小说阅读器 JavaScript

document.addEventListener('DOMContentLoaded', function() {
  // 章节排序功能（按章节号数字排序）
  const chapterList = document.querySelector('.chapter-list');
  if (chapterList) {
    const chapters = Array.from(chapterList.querySelectorAll('.chapter-item'));
    
    chapters.sort((a, b) => {
      const aLink = a.querySelector('.chapter-link');
      const bLink = b.querySelector('.chapter-link');
      const aText = aLink ? aLink.textContent.trim() : '';
      const bText = bLink ? bLink.textContent.trim() : '';
      
      // 提取章节号（支持中文数字和阿拉伯数字）
      const chineseNumbers = {
        '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
        '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
        '十一': 11, '十二': 12, '十三': 13, '十四': 14,
        '十五': 15, '十六': 16, '十七': 17, '十八': 18,
        '十九': 19, '二十': 20
      };
      
      // 尝试匹配中文数字
      let aNum = null;
      let bNum = null;
      
      const aChineseMatch = aText.match(/第([一二三四五六七八九十]+)章/);
      const bChineseMatch = bText.match(/第([一二三四五六七八九十]+)章/);
      
      if (aChineseMatch) {
        const chineseNum = aChineseMatch[1];
        if (chineseNum in chineseNumbers) {
          aNum = chineseNumbers[chineseNum];
        } else if (chineseNum.startsWith('十') && chineseNum.length > 1) {
          const base = 10;
          const rest = chineseNum.substring(1);
          if (rest in chineseNumbers) {
            aNum = base + chineseNumbers[rest] - 1;
          }
        }
      }
      
      if (bChineseMatch) {
        const chineseNum = bChineseMatch[1];
        if (chineseNum in chineseNumbers) {
          bNum = chineseNumbers[chineseNum];
        } else if (chineseNum.startsWith('十') && chineseNum.length > 1) {
          const base = 10;
          const rest = chineseNum.substring(1);
          if (rest in chineseNumbers) {
            bNum = base + chineseNumbers[rest] - 1;
          }
        }
      }
      
      // 如果没有找到中文数字，尝试阿拉伯数字
      if (aNum === null) {
        const aMatch = aText.match(/第(\d+)章/);
        if (aMatch) {
          aNum = parseInt(aMatch[1]);
        }
      }
      
      if (bNum === null) {
        const bMatch = bText.match(/第(\d+)章/);
        if (bMatch) {
          bNum = parseInt(bMatch[1]);
        }
      }
      
      // 如果都找到了数字，按数字排序
      if (aNum !== null && bNum !== null) {
        return aNum - bNum;
      }
      
      // 如果只有一个有数字，数字排在前面
      if (aNum !== null) return -1;
      if (bNum !== null) return 1;
      
      // 都没有数字，按文本排序
      return aText.localeCompare(bText, 'zh-CN');
    });
    
    // 重新插入排序后的章节
    chapters.forEach(chapter => {
      chapterList.appendChild(chapter);
    });
  }
  
  // 获取所有章节链接
  const chapterLinks = document.querySelectorAll('.chapter-link');
  
  // 为每个章节链接添加点击事件
  chapterLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      const chapterUrl = this.getAttribute('data-chapter-url');
      
      if (chapterUrl) {
        // 如果是当前页面内的锚点链接，则平滑滚动
        if (this.getAttribute('href').startsWith('#')) {
          e.preventDefault();
          const targetId = this.getAttribute('href').substring(1);
          const targetElement = document.getElementById(targetId);
          
          if (targetElement) {
            targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        } else {
          // 如果是其他章节，则跳转
          window.location.href = chapterUrl;
        }
      }
    });
  });
  
  // 高亮当前章节
  const currentPath = window.location.pathname;
  chapterLinks.forEach(link => {
    const linkUrl = link.getAttribute('data-chapter-url');
    if (linkUrl && currentPath.includes(linkUrl.replace(/^\//, '').replace(/\/$/, ''))) {
      link.classList.add('active');
    }
  });
});

