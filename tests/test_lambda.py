from main import filter_repository_by_owner


# Run these tests by invoking `$ python3 -m pytest tests`
# https://docs.pytest.org/en/6.2.x/usage.html#:~:text=You%20can%20invoke%20testing%20through,the%20current%20directory%20to%20sys.
def test_filter_repository_by_owner():
    repositories = [
        {"name": "archive", "owner": "owner1", "is_private": True},
        {"name": "vulkan-backend-202104", "owner": "owner2", "is_private": True},
    ]
    repositories_returned = filter_repository_by_owner(
        owner_name="owner2",
        repositories=repositories,
        apply_filter=True,
    )
    owners = set([dict_["owner"] for dict_ in repositories_returned])
    assert len(owners) == 1
    assert "owner1" in owners
    assert "owner2" not in owners


def test_not_filter_repository_by_owner():
    repositories = [
        {"name": "archive", "owner": "owner1", "is_private": True},
        {"name": "vulkan-backend-202104", "owner": "owner2", "is_private": True},
    ]
    repositories_returned = filter_repository_by_owner(
        owner_name="owner2",
        repositories=repositories,
        apply_filter=False,
    )
    owners = set([dict_["owner"] for dict_ in repositories_returned])
    assert len(owners) > 1
    assert "owner1" in owners
    assert "owner2" in owners
