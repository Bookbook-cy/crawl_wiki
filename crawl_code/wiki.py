import wikipediaapi

wiki = wikipediaapi.Wikipedia(user_agent="MyWikipediaBot/1.0 (myemail@example.com)", language="zh")
page = wiki.page("中華民國節日與歲時列表")
page1 = wiki.page("中華民國節日與歲時列表")


if page.exists():
    print(f"标题: {page.title}")
    # print(f"页面摘要: {page.summary}")
    print(f"完整内容: {page.text[:]}...")  # 只显示前 500 个字符
    print(f"{page.sections}")
    # 获得列表的内容

else:
    print("页面不存在")
